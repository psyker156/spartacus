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

from Configuration.Configuration import MEMORY_START_AT, \
                                        MEMORY_CELL_INITIAL_VALUE, \
                                        MEMORY_END_AT

__author__ = "CSE"
__copyright__ = "Copyright 2015, CSE"
__credits__ = ["CSE"]
__license__ = "GPL"
__version__ = "2.1"
__maintainer__ = "CSE"
__status__ = "Dev"


class MemoryArray:
    """
    MemoryArray class is used to group and manage access to the MemoryCell composing
    Capua memory array. It will extract MemoryCells based on address and required parameter
    IT WILL NOT manage read and write values to the memory itself. It only provides the memory!
    Read and Write access are managed by whatever code need such access to extracted MemoryCells.
    """

    _memoryCellArray = None  # MemoryCells are kept in there

    def __init__(self):
        """
        This will initialize the whole memory cell array. No parameters required, we want Capua
        environment to be configurable by the user with minimal code change.
        Configuration for memory cell array are in Configuration.Configuration
        """
        self._memoryCellArray = [
            MEMORY_CELL_INITIAL_VALUE
            for x in range(MEMORY_START_AT, MEMORY_END_AT)
        ]

    def readMemory(self, address, length=1):
        """
        This method allows to read a slice of contiguous memory
        :param address: int, Address for which access is required
        :param length: int length of the required extraction
        :return: list of MemoryCell that are contiguous in memory
        """
        # Check memory access is ok
        self._validateAddressForLengthAccess(address, length)

        # Memory extraction from base
        baseIndex = self._computeArrayIndexFromAddress(address)
        memorySlice = self._memoryCellArray[baseIndex:baseIndex + length]

        return memorySlice

    def writeMemory(self, address, values):
        """
        This method will overwrite values from a given address
        :param address: int, the address where the overwrite is to happen
        :param values: int list, a list containing values to be writen in memory
        :param length: int, length of the write operation
        :return: none
        """
        length = len(values)

        # Check memory access is ok
        self._validateAddressForLengthAccess(address, length)

        # Do memory access
        base = self._computeArrayIndexFromAddress(address)
        self._memoryCellArray[base:base + length] = values

    def _validateAddressForLengthAccess(self, address, length):
        """
        This method does memory range access validation. It will validate
        that a given memory address and length are actually available on
        the system. In case an address/length it out of memory range a
        MemoryError is raised.
        :param address: int, the address where the memory check must start
        :param length: int, the length for the memory check
        :return: none
        """
        lengthLimit = MEMORY_END_AT - address
        if address < MEMORY_START_AT or length <= 0 or length > lengthLimit:
            raise MemoryError("Access reaching out of bound of memory for address: {}".format(hex(address)))

    def directMemoryCellAccess(self, address):
        """
        This will return the memory cell so caller can work directly on the cell itself instead of
        using the memory array to access the cell. Allow for more flexible access to memory.
        :param address: int, Address for which access is requires
        :return: int, memory cell (8 bits) required by accessing program
        """
        index = self._computeArrayIndexFromAddress(address)
        return self._memoryCellArray[index]

    def _computeArrayIndexFromAddress(self, address):
        """
        Will compute the index required to access a given memory cell into the memory cell array.
        :param address: The address for which we want the index
        :return: int representing the index at which an address can be accessed
        """
        index = None

        # First, is the address in a valid range
        if MEMORY_START_AT > address or address >= MEMORY_END_AT:
            # Address out of bounds!
            raise MemoryError("Address out of bounds of memory {}".format(str(address)))

        # Calculate the actual index in memory array
        index = address - MEMORY_START_AT

        return index
