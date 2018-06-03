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

import unittest

from CapuaEnvironment.MemoryArray.MemoryArray import MemoryArray
from CapuaEnvironment.VirtualMemoryManager.VirtualMemoryManager import VirtualMemoryManager
from Configuration.Configuration import MEMORY_START_AT, \
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


class TestVirtualMemoryManager(unittest.TestCase):

    vmm = VirtualMemoryManager(MemoryArray())

    def test_init(self):
        """
        Validates the correct working of the __init__ method.
        """
        self.assertRaises(RuntimeError, VirtualMemoryManager, None)

    def test_translationCacheLookup(self):
        """
        Validates the correct working of the translationCacheLookup method.
        def translationCacheLookup(self, virtualAddress, vmr):
        """
        # Setting up a tt for the test
        self.vmm.ma.writeMemory(MEMORY_START_AT, [0x08, 0x00])
        self.vmm.ma.writeMemory(MEMORY_START_AT + 2, [0x08, 0x01])
        self.vmm.ma.writeMemory(MEMORY_START_AT + 4, [0x08, 0x02])
        self.vmm.ma.writeMemory(MEMORY_START_AT + 6, [0x08, 0x03])
        self.vmm.ma.writeMemory(MEMORY_START_AT + 8, [0x08, 0x04])

        ttEntry = self.vmm.getTTEntryForAddress(0x80000, MEMORY_START_AT)
        physicalAddress = self.vmm.translateVirtualToPhysicalAddress(0x80000, ttEntry)

        cacheLookupAddress = self.vmm.translationCacheLookup(0x80001)
        self.assertEqual(0x40080001, cacheLookupAddress[0])     # The address
        self.assertEqual(0x0801, cacheLookupAddress[1])         # The ttEntry

        self.vmm.tlbFlush()
        cacheLookupAddress = self.vmm.translationCacheLookup(0x80001)
        self.assertEqual(None, cacheLookupAddress)              # No translation available

    def test_translateVirtualToPhysicalAddress(self):
        """
        Validates the correct working of the translateVirtualToPhysicalAddress method.
        def translateVirtualToPhysicalAddress(self, virtualAddress, ttEntry):
        """
        # Setting up a tt for the test
        self.vmm.ma.writeMemory(MEMORY_START_AT, [0x08, 0x00])
        self.vmm.ma.writeMemory(MEMORY_START_AT + 2, [0x08, 0x01])
        self.vmm.ma.writeMemory(MEMORY_START_AT + 4, [0x08, 0x02])
        self.vmm.ma.writeMemory(MEMORY_START_AT + 6, [0x08, 0x03])
        self.vmm.ma.writeMemory(MEMORY_START_AT + 8, [0x08, 0x04])

        ttEntry = self.vmm.getTTEntryForAddress(0x80000, MEMORY_START_AT)
        physicalAddress = self.vmm.translateVirtualToPhysicalAddress(0x80000, ttEntry)
        self.assertEqual(0x40080000, physicalAddress)

        ttEntry = self.vmm.getTTEntryForAddress(0x80200, MEMORY_START_AT)
        physicalAddress = self.vmm.translateVirtualToPhysicalAddress(0x80200, ttEntry)
        self.assertEqual(0x40080200, physicalAddress)

        ttEntry = self.vmm.getTTEntryForAddress(0x100000, MEMORY_START_AT)  # This should be the third entry
        physicalAddress = self.vmm.translateVirtualToPhysicalAddress(0x100000, ttEntry)
        self.assertEqual(0x40100000, physicalAddress)

        ttEntry = self.vmm.getTTEntryForAddress(0x180000, MEMORY_START_AT)  # This should be the fourth entry
        physicalAddress = self.vmm.translateVirtualToPhysicalAddress(0x180000, ttEntry)
        self.assertEqual(0x40180000, physicalAddress)

        ttEntry = self.vmm.getTTEntryForAddress(0x200000, MEMORY_START_AT)  # This should be the fifth entry
        physicalAddress = self.vmm.translateVirtualToPhysicalAddress(0x200000, ttEntry)
        self.assertEqual(0x40200000, physicalAddress)


    def test_getTTEntryForAddress(self):
        """
        Validates the correct working of the getTTEntryForAddress method.
        def getTTEntryForAddress(self, virtualAddress, vmr):
        """
        # Setting up a tt for the test
        self.vmm.ma.writeMemory(MEMORY_START_AT, [0x08, 0x00])
        self.vmm.ma.writeMemory(MEMORY_START_AT + 2, [0x08, 0x01])
        self.vmm.ma.writeMemory(MEMORY_START_AT + 4, [0x08, 0x02])
        self.vmm.ma.writeMemory(MEMORY_START_AT + 6, [0x08, 0x03])
        self.vmm.ma.writeMemory(MEMORY_START_AT + 8, [0x08, 0x04])

        ttEntry = self.vmm.getTTEntryForAddress(0x80000, MEMORY_START_AT)  # This should be the second entry
        self.assertEqual(0x0801, ttEntry)

        ttEntry = self.vmm.getTTEntryForAddress(0x80001, MEMORY_START_AT)  # This should be the second entry
        self.assertEqual(0x0801, ttEntry)

        ttEntry = self.vmm.getTTEntryForAddress(0xFFFFF, MEMORY_START_AT)  # This should be the second entry
        self.assertEqual(0x0801, ttEntry)

        ttEntry = self.vmm.getTTEntryForAddress(0x100000, MEMORY_START_AT)  # This should be the third entry
        self.assertEqual(0x0802, ttEntry)

        ttEntry = self.vmm.getTTEntryForAddress(0x100001, MEMORY_START_AT)  # This should be the third entry
        self.assertEqual(0x0802, ttEntry)

        ttEntry = self.vmm.getTTEntryForAddress(0x17FFFF, MEMORY_START_AT)  # This should be the third entry
        self.assertEqual(0x0802, ttEntry)

        ttEntry = self.vmm.getTTEntryForAddress(0x180000, MEMORY_START_AT)  # This should be the fourth entry
        self.assertEqual(0x0803, ttEntry)

        ttEntry = self.vmm.getTTEntryForAddress(0x180001, MEMORY_START_AT)  # This should be the fourth entry
        self.assertEqual(0x0803, ttEntry)

        ttEntry = self.vmm.getTTEntryForAddress(0x1FFFFF, MEMORY_START_AT)  # This should be the fourth entry
        self.assertEqual(0x0803, ttEntry)

        ttEntry = self.vmm.getTTEntryForAddress(0x200000, MEMORY_START_AT)  # This should be the fifth entry
        self.assertEqual(0x0804, ttEntry)

        ttEntry = self.vmm.getTTEntryForAddress(0x200001, MEMORY_START_AT)  # This should be the fifth entry
        self.assertEqual(0x0804, ttEntry)

        ttEntry = self.vmm.getTTEntryForAddress(0x27FFFF, MEMORY_START_AT)  # This should be the fifth entry
        self.assertEqual(0x0804, ttEntry)

    def test_processTranslation(self):
        """
        Validates the correct working of the tlbFlush method.
        processTranslation(self, address, vmr):
        """
        self.vmm.ma.writeMemory(MEMORY_START_AT, [0x08, 0x00])
        self.vmm.ma.writeMemory(MEMORY_START_AT + 2, [0x08, 0x01])
        self.vmm.ma.writeMemory(MEMORY_START_AT + 4, [0x08, 0x02])
        self.vmm.ma.writeMemory(MEMORY_START_AT + 6, [0x08, 0x03])
        self.vmm.ma.writeMemory(MEMORY_START_AT + 8, [0x08, 0x04])

        physicalAddress = self.vmm.processTranslation(0x80000, MEMORY_START_AT)
        self.assertEqual(0x40080000, physicalAddress)

    def test_tlbFlush(self):
        """
        Validates the correct working of the tlbFlush method.
        def tlbFlush(self):
        """
        # Setting up a tt for the test
        self.vmm.ma.writeMemory(MEMORY_START_AT, [0x08, 0x00])
        self.vmm.ma.writeMemory(MEMORY_START_AT + 2, [0x08, 0x01])
        self.vmm.ma.writeMemory(MEMORY_START_AT + 4, [0x08, 0x02])
        self.vmm.ma.writeMemory(MEMORY_START_AT + 6, [0x08, 0x03])
        self.vmm.ma.writeMemory(MEMORY_START_AT + 8, [0x08, 0x04])

        ttEntry = self.vmm.getTTEntryForAddress(0x80000, MEMORY_START_AT)
        physicalAddress = self.vmm.translateVirtualToPhysicalAddress(0x80000, ttEntry)

        self.assertEqual(1, len(self.vmm.tlb.keys()))

        self.vmm.tlbFlush()
        self.assertEqual(0, len(self.vmm.tlb.keys()))

    def test_validateAccessRequirements(self):
        """
        Validates the correct working of the validateAccessRequirements method.
        processTranslation(self, address, vmr):
        """
        self.vmm.ma.writeMemory(MEMORY_START_AT,
                                [(0x08 | (0b100 << 5)), 0x00])     # Set as executable not available
        self.vmm.ma.writeMemory(MEMORY_START_AT + 2,
                                [(0x08 | (0b110 << 5)), 0x01])     # Set as executable + privileged not available
        self.vmm.ma.writeMemory(MEMORY_START_AT + 4,
                                [(0x08 | (0b111 << 5)), 0x02])     # Set as executable + privileged + available
        self.vmm.ma.writeMemory(MEMORY_START_AT + 6,
                                [(0x08 | (0b001 << 5)), 0x03])     # Set as no execute + available
        self.vmm.ma.writeMemory(MEMORY_START_AT + 8,
                                [(0x08 | (0b101 << 5)), 0x04])     # Set as execute + available

        accessLevel = self.vmm.validateAccessRequirements(True, [0x80000, 0x80004], [], MEMORY_START_AT)
        self.assertEqual(EXCEPTION_PAGE_NOT_AVAILABLE, accessLevel)

        accessLevel = self.vmm.validateAccessRequirements(True, [0x100000, 0x100004], [0x1000FF], MEMORY_START_AT)
        self.assertEqual(ACCESS_GRANTED, accessLevel)

        accessLevel = self.vmm.validateAccessRequirements(False, [0x100000, 0x100004], [0x1000FF], MEMORY_START_AT)
        self.assertEqual(EXCEPTION_MEMORY_ACCESS_DENIED, accessLevel)

        accessLevel = self.vmm.validateAccessRequirements(True, [], [0x1000FF], MEMORY_START_AT)
        self.assertEqual(ACCESS_GRANTED, accessLevel)

        accessLevel = self.vmm.validateAccessRequirements(False, [], [0x1000FF], MEMORY_START_AT)
        self.assertEqual(EXCEPTION_MEMORY_ACCESS_DENIED, accessLevel)

        accessLevel = self.vmm.validateAccessRequirements(False, [0x200000, 0x200004], [0x2000FF], MEMORY_START_AT)
        self.assertEqual(ACCESS_GRANTED, accessLevel)

        accessLevel = self.vmm.validateAccessRequirements(True, [], [0x2000FF], MEMORY_START_AT)
        self.assertEqual(ACCESS_GRANTED, accessLevel)

        accessLevel = self.vmm.validateAccessRequirements(False, [], [0x2000FF], MEMORY_START_AT)
        self.assertEqual(ACCESS_GRANTED, accessLevel)



    def test_ttEntryIsExecutable(self):
        """
        Validates the correct working of the ttEntryIsExecutable method.
        def ttEntryIsExecutable(self, ttEntry):
        """
        self.assertEqual(True, self.vmm.ttEntryIsExecutable(0x8000))    # See comments in VirtualMemoryManager.py
        self.assertEqual(False, self.vmm.ttEntryIsExecutable(0x2000))

    def test_ttEntryIsPriviledged(self):
        """
        Validates the correct working of the ttEntryIsPriviledged method.
        def ttEntryIsPriviledged(self, ttEntry):
        """
        self.assertEqual(True, self.vmm.ttEntryIsPriviledged(0x4000))   # See comments in VirtualMemoryManager.py
        self.assertEqual(False, self.vmm.ttEntryIsPriviledged(0x8000))

    def test_ttEntryIsAvailable(self):
        """
        Validates the correct working of the ttEntryIsAvailable method.
        def ttEntryIsAvailable(self, ttEntry):
        """
        self.assertEqual(True, self.vmm.ttEntryIsAvailable(0x2000))     # See comments in VirtualMemoryManager.py
        self.assertEqual(False, self.vmm.ttEntryIsAvailable(0x4000))
