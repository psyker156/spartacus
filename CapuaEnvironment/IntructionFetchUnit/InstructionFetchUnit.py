#!/usr/bin/env python
#  -*- coding: <utf-8> -*-

"""
This file is part of Spartacus project
Copyright (C) 2016  CSE

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

from CapuaEnvironment.Instruction.Instruction import Instruction
from CapuaEnvironment.IntructionFetchUnit.FormDescription import formDescription
from CapuaEnvironment.IOComponent.MemoryIOController import MemoryIOController
from Configuration.Configuration import MEMORY_START_AT, \
                                        MEMORY_MAXIMUM_READ_WRITE_SIZE, \
                                        VIRTUAL_NULL, \
                                        EXCEPTION_BAD_INSTRUCTION_FETCH, \
                                        EXCEPTION_NO_EXECUTE_PERMISSION, \
                                        EXCEPTION_MEMORY_ACCESS_DENIED, \
                                        EXCEPTION_PAGE_NOT_AVAILABLE

__author__ = "CSE"
__copyright__ = "Copyright 2015, CSE"
__credits__ = ["CSE"]
__license__ = "GPL"
__version__ = "2.2"
__maintainer__ = "CSE"
__status__ = "Dev"


class InstructionFetchUnit:
    """
    The InstructionFetchUnit is used to extract actual instruction from memory.
    It will build instruction using data extracted from the MemoryArray. In case the
    access to memory is not allowed, memory cells will cause exception to be raised.
    Since it is available, it is also used in the debugger in order to provide code
    disassembling functionality.
    """
    _memoryIOController = None
    _eu = None                  # Need EU access to signal exceptions

    def __init__(self, memoryIOController=None, eu=None):
        """
        Simply initialize an instance of this class... Nothing much to say. Actual logic is elsewhere.
        :param memoryIOController: This has to be a non None MemoryArray
        :param eu: ExecutionUnit to which this fetch unit is attached
        """
        if memoryIOController is None:
            raise RuntimeError("Capua InstructionFetchUnit init error")
        self._memoryIOController = memoryIOController
        if eu is None:
            raise RuntimeError("Capua InstructionFetchUnit init error")
        self._eu = eu

    def fetchInstructionAtAddress(self, address=MEMORY_START_AT, vmr=VIRTUAL_NULL):
        """
        This is the high level fetching method for this class. It is the only one
        that should be called by the user. Note that the address is NOT validated here
        since the actual validation logic lays in the MemoryIOController, MemoryArray
        and MemoryCell code
        :param address: int, The address where the fetch needs to happen
        :return: Instruction, nextInstructionAddress
        """

        instruction = None
        nextInstructionAddress = None
        executeAccessGranted = True
        isPrivileged = False
        isAvailable = True

        # First thing, do we have execute access at the given address?
        if vmr != VIRTUAL_NULL:
            ttEntry = self._memoryIOController.virtualMemoryManager.getTTEntryForAddress(address, vmr)
            executeAccessGranted = self._memoryIOController.virtualMemoryManager.ttEntryIsExecutable(ttEntry)
            isPrivileged = self._memoryIOController.virtualMemoryManager.ttEntryIsPriviledged(ttEntry)
            isAvailable = self._memoryIOController.virtualMemoryManager.ttEntryIsAvailable(ttEntry)

        if not executeAccessGranted:
            # an illegal memory access just happened!
            self._eu.signalHardwareException(interruptNumber=EXCEPTION_NO_EXECUTE_PERMISSION,
                                             exceptionCode=self._eu.I,
                                             faultyInstruction=self._eu.I)

        if isPrivileged and not self._eu.currentPrivilegeLevel:
            # we are about to fetch from a privileged part of memory while we are not privileged
            self._eu.signalHardwareException(interruptNumber=EXCEPTION_MEMORY_ACCESS_DENIED,
                                             exceptionCode=self._eu.I,
                                             faultyInstruction=self._eu.I)

        if not isAvailable:
            # we are about to fetch an instruction in a page that is not loaded in memory
            self._eu.signalHardwareException(interruptNumber=EXCEPTION_PAGE_NOT_AVAILABLE,
                                             exceptionCode=self._eu.I,
                                             faultyInstruction=self._eu.I)

        # Execute access granted, fetch the instruction!
        instructionForm = self._fetchInstructionFormAtAddress(address)

        if instructionForm is not None:
            instruction = self._fetchInstructionAtAddressUsingForm(address, instructionForm)
            nextInstructionAddress = address + instructionForm["length"]

        return instruction, nextInstructionAddress

    def _fetchInstructionFormAtAddress(self, address=MEMORY_START_AT):
        """
        This will fetch the first byte of the instruction at given address. Once fetched,
        it uses that first byte to determine instruction format. Returns information on
        the instruction format so that the whole instruction can be extracted from memory
        :param address:
        :return:
        """
        instructionForm = None
        mc = self._memoryIOController.memoryReadAtAddressForLength(address, 1)
        value = mc & 0xff   # Making sure we have an 8 bits value

        # Extracting type and instruction codes
        typeCode = (value & 0b11110000) >> 4
        instructionCode = value & 0b00001111

        for form in formDescription:
            if typeCode == formDescription[form]["typeCode"]:
                if instructionCode in formDescription[form]["listing"]:
                    # We found the correct form!
                    instructionForm = formDescription[form]
                    break
        if instructionForm is None:
            # If we are here, no instruction were found that are corresponding
            # a user is trying to execute an invalid instruction!
            self._eu.signalHardwareException(interruptNumber=EXCEPTION_BAD_INSTRUCTION_FETCH,
                                             exceptionCode=0,
                                             faultyInstruction=self._eu.I)

        return instructionForm

    def _fetchInstructionAtAddressUsingForm(self, address=MEMORY_START_AT, form=None):
        """
        This will fetch the complete instruction information and build an instruction instance
        using the extracted data. The instruction instance is returned to calling method
        :param address: Address of the instruction that needs to be fetched
        :param form: The form of the instruction that requires fetching
        :return: An instance of the Instruction class
        """
        instruction = None

        # First, we need to figure how many reads need to happen
        numberOfMaximumReadSizeOperations = form["length"] // MEMORY_MAXIMUM_READ_WRITE_SIZE
        partialReadSize = form["length"] % MEMORY_MAXIMUM_READ_WRITE_SIZE

        # Now we can construct a very big number...
        memoryContent = 0
        readAddress = address
        for i in range(0, numberOfMaximumReadSizeOperations):
            memoryContent <<= MEMORY_MAXIMUM_READ_WRITE_SIZE * 8
            memoryContent |= self._memoryIOController.memoryReadAtAddressForLength(readAddress,
                                                                                   MEMORY_MAXIMUM_READ_WRITE_SIZE)
            readAddress += MEMORY_MAXIMUM_READ_WRITE_SIZE

        memoryContent <<= partialReadSize * 8
        memoryContent |= self._memoryIOController.memoryReadAtAddressForLength(readAddress, partialReadSize)

        # binaryInstruction is now  a big number representing the instruction
        # Time to create the instruction using this big number!
        # Parsing of the details of the instruction will happen in the Instruction class
        instruction = Instruction(memoryContent, form)

        return instruction
