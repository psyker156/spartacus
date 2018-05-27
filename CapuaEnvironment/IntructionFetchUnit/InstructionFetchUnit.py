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
from CapuaEnvironment.MemoryArray.MemoryArray import MemoryArray
from Configuration.Configuration import MEMORY_START_AT

__author__ = "CSE"
__copyright__ = "Copyright 2015, CSE"
__credits__ = ["CSE"]
__license__ = "GPL"
__version__ = "2.1"
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
    _memoryArray = None

    def __init__(self, memoryArray: MemoryArray=None):
        """
        Simply initialize an instance of this class... Nothing much to say. Actual logic is elsewhere.
        :param memoryArray: This has to be a non None MemoryArray
        """
        if memoryArray is None:
            raise RuntimeError("Capua InstructionFetchUnit init error")
        self._memoryArray = memoryArray

    def fetchInstructionAtAddress(self, address=MEMORY_START_AT):
        """
        This is the high level fetching method for this class. It is the only one
        that should be called by the user. Note that the address is NOT validated here
        since the actual validation logic lays in the MemoryIOController, MemoryArray
        and MemoryCell code
        :param address: int, The address where the fetch needs to happen
        :return: Instruction, nextInstructionAddress
        """

        instructionForm = self._fetchInstructionFormAtAddress(address)
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
        mc = self._memoryArray.readMemory(address, 1)[0]
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
            raise ValueError("Invalid instruction detected at address {}".format(hex(address)))

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

        # First, we get the memory bits that we need!
        memorySlice = self._memoryArray.readMemory(address, form["length"])

        # Now, build a big number (as in real big) with the extracted memory
        binaryInstruction = 0
        for mc in memorySlice:
            binaryInstruction <<= 8
            binaryInstruction |= mc & 0xff  # Only 8 bits can be used at a time

        # binaryInstruction is now  a big number representing the instruction
        # Time to create the instruction using this big number!
        # Parsing of the details of the instruction will happen in the Instruction class
        instruction = Instruction(binaryInstruction, form)

        return instruction
