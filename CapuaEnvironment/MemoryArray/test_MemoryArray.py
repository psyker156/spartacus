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

import unittest

from CapuaEnvironment.MemoryArray.MemoryArray import MemoryArray
from Configuration.Configuration import MEMORY_ARRAY_NUMBER_OF_MEMORY_CELL, \
                                        MEMORY_START_AT, \
                                        MEMORY_CELL_INITIAL_VALUE, \
                                        MEMORY_END_AT

__author__ = "CSE"
__copyright__ = "Copyright 2015, CSE"
__credits__ = ["CSE"]
__license__ = "GPL"
__version__ = "2.2"
__maintainer__ = "CSE"
__status__ = "Dev"


class TestMemoryArray(unittest.TestCase):

    ma = MemoryArray()

    def test_init(self):
        """
        Validates good working of the __init__ method for MemoryArray
        """
        ma = MemoryArray()
        self.assertEqual(MEMORY_ARRAY_NUMBER_OF_MEMORY_CELL, len(ma._memoryCellArray))
        for mc in ma.readMemory(MEMORY_START_AT, MEMORY_ARRAY_NUMBER_OF_MEMORY_CELL):
            self.assertEqual(MEMORY_CELL_INITIAL_VALUE, mc)

    def test_readMemory(self):
        """
        Validates good working of the readMemory method for MemoryArray
        """
        self.assertEqual(1,
                         len(self.ma.readMemory(MEMORY_START_AT, 1)))
        self.assertEqual(5,
                         len(self.ma.readMemory(MEMORY_START_AT, 5)))
        self.assertEqual(MEMORY_ARRAY_NUMBER_OF_MEMORY_CELL,
                         len(self.ma.readMemory(MEMORY_START_AT, MEMORY_ARRAY_NUMBER_OF_MEMORY_CELL)))
        self.assertEqual(1,
                         len(self.ma.readMemory(MEMORY_END_AT - 1, 1)))

        self.assertRaises(MemoryError,
                          self.ma.readMemory,
                          MEMORY_END_AT - 5,
                          6)
        self.assertRaises(MemoryError,
                          self.ma.readMemory,
                          MEMORY_START_AT - 1,
                          6)

    def test_writeMemory(self):
        """
        Validates good working of the writeMemory method for MemoryArray
        """
        self.ma.writeMemory(MEMORY_START_AT, [1])
        self.assertEqual(1, self.ma.readMemory(MEMORY_START_AT, 1)[0])

        self.ma.writeMemory(MEMORY_START_AT, [0, 0, 0, 1])
        self.assertEqual(0, self.ma.readMemory(MEMORY_START_AT, 1)[0])
        self.assertEqual(0, self.ma.readMemory(MEMORY_START_AT + 1, 1)[0])
        self.assertEqual(0, self.ma.readMemory(MEMORY_START_AT + 2, 1)[0])
        self.assertEqual(1, self.ma.readMemory(MEMORY_START_AT + 3, 1)[0])

        self.assertRaises(MemoryError,
                          self.ma.writeMemory,
                          MEMORY_END_AT + 5,
                          [1])
        self.assertRaises(MemoryError,
                          self.ma.writeMemory,
                          MEMORY_START_AT - 1,
                          [1])

    def test_validateAddressForLengthAccess(self):
        """
        Validates good working of the _validateAddressForLengthAccess method
        """
        self.assertRaises(MemoryError, self.ma._validateAddressForLengthAccess, MEMORY_START_AT - 1, 1)
        self.assertRaises(MemoryError, self.ma._validateAddressForLengthAccess, MEMORY_START_AT - 1, 4)
        self.assertRaises(MemoryError, self.ma._validateAddressForLengthAccess, MEMORY_END_AT, 1)
        self.assertRaises(MemoryError, self.ma._validateAddressForLengthAccess, MEMORY_START_AT - 1, 2)

    def test_directMemoryCellAccess(self):
        """
        Validates good working of the _directMemoryCellAccess method for MemoryArray
        """
        self.assertIsNotNone(self.ma._directMemoryCellAccess(MEMORY_START_AT))       # Valid memory address
        self.assertIsNotNone(self.ma._directMemoryCellAccess(MEMORY_END_AT - 1))     # Valid memory address
        self.assertRaises(MemoryError, self.ma._directMemoryCellAccess, MEMORY_START_AT - 1)     # Invalid memory access
        self.assertRaises(MemoryError, self.ma._directMemoryCellAccess, MEMORY_END_AT)           # Invalid memory access

    def test_computeArrayIndexFromAddress(self):
        """
        Validates good working of the computeArrayIndexFromAddress method for MemoryArray
        """
        self.assertTrue(self.ma._computeArrayIndexFromAddress(MEMORY_START_AT) >= 0)                     # Valid address
        self.assertTrue(self.ma._computeArrayIndexFromAddress(MEMORY_START_AT +
                                                              MEMORY_ARRAY_NUMBER_OF_MEMORY_CELL -
                                                              1) >= 0)                                   # Valid address
        self.assertRaises(MemoryError,
                          self.ma._computeArrayIndexFromAddress,
                          MEMORY_START_AT - 1)  # Invalid address
        self.assertRaises(MemoryError,
                          self.ma._computeArrayIndexFromAddress,
                          MEMORY_END_AT + 1)  # invalid address


if __name__ == '__main__':
    unittest.main()
