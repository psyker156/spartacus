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

from CapuaEnvironment.ExecutionUnit.ExecutionUnit import ExecutionUnit
from CapuaEnvironment.IntructionFetchUnit.InstructionFetchUnit import InstructionFetchUnit
from CapuaEnvironment.MemoryArray.MemoryArray import MemoryArray
from CapuaEnvironment.IOComponent.MemoryIOController import MemoryIOController
from Configuration.Configuration import MEMORY_START_AT

__author__ = "CSE"
__copyright__ = "Copyright 2015, CSE"
__credits__ = ["CSE"]
__license__ = "GPL"
__version__ = "2.0"
__maintainer__ = "CSE"
__status__ = "Dev"


class TestMemoryIOController(unittest.TestCase):

    ma = MemoryArray()
    mioc = MemoryIOController(ma)
    eu = ExecutionUnit("System")
    ifu = InstructionFetchUnit(mioc, eu)
    eu.ifu = ifu
    eu.mioc = mioc
    eu.mioc.eu = eu

    def test_init(self):
        """
        Validates good working of the __init__ method for MemoryIOController
        """
        ma = MemoryArray()
        self.assertRaises(RuntimeError, MemoryIOController)
        self.assertRaises(RuntimeError, MemoryIOController, "invalid")
        self.assertEqual(MemoryIOController, type(MemoryIOController(ma)))

    def test_memoryReadWriteAtAddressForLength(self):
        """
        Validates good working of the memoryReadAtAddressForLength memoryWriteAtAddressForLength
        method for MemoryIOController
        memoryWriteAtAddressForLength(self, address=0x00, length=4, value=0x00)
        memoryReadAtAddressForLength(self, address=0x00, length=4)
        """
        self.mioc.memoryWriteAtAddressForLength(MEMORY_START_AT, 1, 0x01)
        memValue = self.mioc.memoryReadAtAddressForLength(MEMORY_START_AT, 1)
        self.assertEqual(0x01, memValue)

        self.mioc.memoryWriteAtAddressForLength(MEMORY_START_AT, 2, 0x0202)
        memValue = self.mioc.memoryReadAtAddressForLength(MEMORY_START_AT, 2)
        self.assertEqual(0x0202, memValue)

        memValue = self.mioc.memoryReadAtAddressForLength(MEMORY_START_AT + 1, 1)
        self.assertEqual(0x02, memValue)

        self.mioc.memoryWriteAtAddressForLength(MEMORY_START_AT, 3, 0x030303)
        memValue = self.mioc.memoryReadAtAddressForLength(MEMORY_START_AT, 3)
        self.assertEqual(0x030303, memValue)

        memValue = self.mioc.memoryReadAtAddressForLength(MEMORY_START_AT + 1, 2)
        self.assertEqual(0x0303, memValue)

        self.mioc.memoryWriteAtAddressForLength(MEMORY_START_AT, 4, 0x04040404)
        memValue = self.mioc.memoryReadAtAddressForLength(MEMORY_START_AT, 4)
        self.assertEqual(0x04040404, memValue)

        memValue = self.mioc.memoryReadAtAddressForLength(MEMORY_START_AT + 1, 3)
        self.assertEqual(0x040404, memValue)

        memValue = self.mioc.memoryReadAtAddressForLength(MEMORY_START_AT + 1, 4)
        self.assertEqual(0x040404FF, memValue)

    def test_passMemoryReadWriteToMemoryMappedHardware(self):
        """
        Validates good working of the passMemoryReadWriteToMemoryMappedHardware method for MemoryIOController
        passMemoryReadWriteToMemoryMappedHardware(self, address=0x00, length=4, value=0x00, isWrite=False)
        """
        self.assertRaises(MemoryError, self.mioc._passMemoryReadWriteToMemoryMappedHardware)

    def test_prepareNumericValueToBeWrittenToMemory(self):
        """
        Validates good working of the passMemoryReadWriteToMemoryMappedHardware method for MemoryIOController
        _prepareNumericValueToBeWrittenToMemory(self, length=0, value=0)
        """
        self.assertEqual(1, len(self.mioc._prepareNumericValueToBeWrittenToMemory(1, 0xff)))
        self.assertEqual(2, len(self.mioc._prepareNumericValueToBeWrittenToMemory(2, 0xffff)))
        self.assertEqual(3, len(self.mioc._prepareNumericValueToBeWrittenToMemory(3, 0xffffff)))
        self.assertEqual(4, len(self.mioc._prepareNumericValueToBeWrittenToMemory(4, 0xffffffff)))
        self.assertEqual(4, len(self.mioc._prepareNumericValueToBeWrittenToMemory(4, 0xff)))
        self.assertRaises(ValueError, self.mioc._prepareNumericValueToBeWrittenToMemory, 1, 0xffff)
