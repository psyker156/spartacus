#!/usr/bin/env python
#  -*- coding: <utf-8> -*-

"""
This file is part of Spartacus project
Copyright (C) 2018  CSE

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

from CapuaEnvironment.MemoryArray.MemoryArray import MemoryArray
from Configuration.Configuration import VIRTUAL_PAGE_MASK, \
                                        VIRTUAL_ADDRESS_MASK, \
                                        VIRTUAL_TABLE_ENTRY_MASK, \
                                        VIRTUAL_EXECUTABLE_FLAG, \
                                        VIRTUAL_PRIVILEGED_FLAG, \
                                        VIRTUAL_AVAILABLE_FLAG, \
                                        EXCEPTION_NO_EXECUTE_PERMISSION, \
                                        EXCEPTION_PAGE_NOT_AVAILABLE, \
                                        EXCEPTION_MEMORY_ACCESS_DENIED, \
                                        ACCESS_GRANTED

__author__ = "CSE"
__copyright__ = "Copyright 2018, CSE"
__credits__ = ["CSE"]
__license__ = "GPL"
__version__ = "2.0"
__maintainer__ = "CSE"
__status__ = "Dev"


class VirtualMemoryManager:
    """
    VirtualMemoryManager class aims at doing the translation work
    between virtual and physical memory address. When an access
    is done into memory by the MemoryIOController, this one calls
    into the VirtualMemoryManager in order to get the translation
    from virtual address to physical if such a translation is
    required.

    Important note: This class is NOT responsible for managing concurrent
    access to the memory array. This management can easily happen in the
    MemoryIOController. This on is therefore responsible for this task.

    VirtualMemory system organisation:
    Each page of memory is 512KB long. This is to ensure that only a limited
    number of entries are required for the translation. Also, a larger page
    allows to have a single translation lever.

    Each core (ExecutionUnit) will have a Virtual Memory Register (VMR) register.
    That register points to a physical address where a Translation Table (TT) can
    be found. That table contains a maximum of 8192 entries. Each entry is 16 bits
    long. Each entry is of the following format:
    -------------------------------------------------------
    | E | P | A |       Page Physical Base (PPB)          |
    -------------------------------------------------------
     15  14  13  12                                      0

     E - Bit #15 indicates if a page is executable
     P - Bit #14 indicates if a page is privileged (for future development and addition of privilege level)
     A - Bit #13 indicates if a page is available in memory
     PPB - Bits #12 - #0, total of 13 bits, gives the physical address (512KB alignment) of a given page

     Given this structure, the 13 bits present in a PPB for a given virtual address are used
     to replace the 13 most significant bits of a virtual address in forming a physical address.

     This single level translation allows to create a simple yet usable virtual memory management
     scheme that is easy to understand and implement. This is inline with the stated Spartacus
     goal to be used as an educative tool.
    """

    ma = None   # MemoryArray used by this VirtualMemoryManager
    tlb = {}    # Translation Look Aside buffer - Used to speed up memory translation

    def __init__(self, memoryArray: MemoryArray=None):
        """
        Simple initialisation, this class is dependant on the presence of a memory array
        for it to work properly.
        :param memoryArray: A valid MemoryArray
        """
        if memoryArray is None or type(memoryArray) is not MemoryArray:
            raise RuntimeError("Capua VirtualMemoryManager Error - Setting up memoryArray")

        self.ma = memoryArray

    def translationCacheLookup(self, virtualAddress):
        """
        This method is used for a quick translation using a translation cache
        managed by this instance of VirtualMemoryManager
        :param virtualAddress: int, the address in need of being translated
        :param vmr: int, the vmr for which a translation is being asked
        :return: tuple, (address, ttEntry) tuple
        """
        returnValue = None
        entryBeingLookedUp = virtualAddress & VIRTUAL_PAGE_MASK     # Removes the page offset part to only keep page

        if entryBeingLookedUp in self.tlb.keys():
            # Following replaces the virtual page offset with the physical page offset
            # found inside the tlb.
            tlbResult = self.tlb[entryBeingLookedUp]
            translatedAddress = tlbResult[0] | (virtualAddress & VIRTUAL_ADDRESS_MASK)
            returnValue = (translatedAddress, tlbResult[1])

        return returnValue

    def translateVirtualToPhysicalAddress(self, virtualAddress, ttEntry):
        """
        This is the main method of this class. This does the actual translation
        by parsing the virtualAddress and translation structure.
        :param virtualAddress: int, the address in need of being translated
        :param ttEntry: int, A specific translation table entry
        :return: int, the translated physical address - This can be used by the memory system
        """
        filteredVirtualAddress = virtualAddress & VIRTUAL_ADDRESS_MASK  # This only keeps the page offset part
        virtualPage = (virtualAddress & VIRTUAL_PAGE_MASK)
        physicalPage = (ttEntry & VIRTUAL_TABLE_ENTRY_MASK) << 19

        # The physical page can now be added to the tlb for a given vmr
        self.tlb[virtualPage] = (physicalPage, ttEntry)

        # Physical address is constructed from the physical page and page offset
        return physicalPage | filteredVirtualAddress

    def getTTEntryForAddress(self, virtualAddress, vmr):
        """
        This method returns the 16 bits T.Table entry that is required to
        translate a given address.
        :param virtualAddress: int, the address for which we are trying to get the T.Table entry
        :param vmr: int, the physical address where the translation table can be found
        :return: int, the translation table entry related to a given address
        """
        # First, we need to figure out the offset in the table
        entryOffset = virtualAddress >> 19      # 19 because addresses are 32 bits and top 13 are used for translation
        entryOffset *= 2        # Each entry is 2 byte long

        # Now we can read 2 bytes in memory
        entryList = self.ma.readMemory(vmr + entryOffset, 2)
        ttentry = (entryList[0] << 8) | entryList[1]
        return ttentry

    def processTranslation(self, address, vmr):
        """
        This is a "unified method" that will run through the process of
        address translation in a single call.
        :param address: int, the address in need of translation
        :param vmr: int, the address of the translation table to be used
        :return: int, the translated address
        """
        ttEntry = self.getTTEntryForAddress(address, vmr)
        physicalAddress = self.translateVirtualToPhysicalAddress(address, ttEntry)
        return physicalAddress

    def tlbFlush(self):
        """
        This will clear out the tlb.
        :return:
        """
        self.tlb = {}

    def validateAccessRequirements(self, privileged=True, execute=[], available=[], vmr=0):
        """
        This is to be called for bulk validation of access requirements.
        This will mostly be used by execution unit prior to running instructions.
        :param privileged: bool, is the calling code is privileged
        :param execute: list of ints, list of addresses requiring execute access
        :param available: list of ints, list of addresses requiring general access (no need to repeat execute here)
        :param vmr: int, the address of the translation table to be used
        :return: int, an exception code > 0 indicating an exception (in priority) if 1 access is not validated
        """
        if vmr == 0:
            # No VMR set all access granted
            return ACCESS_GRANTED

        allEntries = []

        # First priority is execution permission
        for address in execute:
            ttEntry = self.getTTEntryForAddress(address, vmr)
            accessible = ttEntry & VIRTUAL_EXECUTABLE_FLAG

            if not accessible:
                return EXCEPTION_NO_EXECUTE_PERMISSION
            allEntries.append(ttEntry)

        # Then availability
        allAddresses = available + execute
        for address in allAddresses:
            ttEntry = self.getTTEntryForAddress(address, vmr)
            accessible = ttEntry & VIRTUAL_AVAILABLE_FLAG

            if not accessible:
                return EXCEPTION_PAGE_NOT_AVAILABLE
            allEntries.append(ttEntry)

        # Last priority is privileged access
        for ttEntry in allEntries:
            privilegedIsRequired = ttEntry & VIRTUAL_PRIVILEGED_FLAG
            if privilegedIsRequired and not privileged:
                return EXCEPTION_MEMORY_ACCESS_DENIED

        # If we are here, access is granted!
        return ACCESS_GRANTED

    def ttEntryIsExecutable(self, ttEntry):
        """
        This checks if a given ttEntry allows for code execution or not
        :param ttEntry: int, a valid Translation Table Entry
        :return: True if executable False otherwise
        """
        return True if ttEntry & VIRTUAL_EXECUTABLE_FLAG else False

    def ttEntryIsPriviledged(self, ttEntry):
        """
        This checks if a given ttEntry is privileged or not
        :param ttEntry: int, a valid Translation Table Entry
        :return: True if Privileged False otherwise
        """
        return True if ttEntry & VIRTUAL_PRIVILEGED_FLAG else False

    def ttEntryIsAvailable(self, ttEntry):
        """
        This checks if a given ttEntry is present in memory
        :param ttEntry: int, a valid Translation Table Entry
        :return: True if in memory False otherwise
        """
        return True if ttEntry & VIRTUAL_AVAILABLE_FLAG else False
