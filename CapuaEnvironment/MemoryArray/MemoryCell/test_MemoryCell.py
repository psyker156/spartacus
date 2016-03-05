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

from CapuaEnvironment.MemoryArray.MemoryCell.MemoryCell import MemoryCell

__author__ = "CSE"
__copyright__ = "Copyright 2015, CSE"
__credits__ = ["CSE"]
__license__ = "GPL"
__version__ = "1.3"
__maintainer__ = "CSE"
__status__ = "Dev"


class TestMemoryCell(unittest.TestCase):

    mc = MemoryCell()

    def test_init(self):
        """
        Validates good working of the __init__ method for MemoryCell
        """

        # Cell using default values
        mc = None
        mc = MemoryCell()
        self.assertIsNotNone(mc)

    def test_MemoryCellIO(self):
        """
        Validates good working of the writeValue method for MemoryCell
        """

        # Write test, make sure we can write to the cell
        if not self.mc.canWrite():
            self.mc.toggleWrite("Alice")
            self.assertEqual("Alice", self.mc.getLastWriteAccessByValue())
        self.mc.writeValue(0xF, "Bob")
        self.assertEqual("Bob", self.mc.getLastWriteAccessByValue())
        self.assertEqual(self.mc._value, 0xF)
        self.mc.writeValue(0xFF, "Bob")
        self.assertEqual(self.mc._value, 0xFF, "Bob")
        self.assertRaises(ValueError, self.mc.writeValue, 0xFFA, "Bob")  # Too long
        self.assertRaises(ValueError, self.mc.writeValue, 0xFF, b"Bob")  # Bad accessor name

        # Write blocking test, make sure we can't write to the cell
        if self.mc.canWrite():
            self.mc.toggleWrite("Alice")
            self.assertEqual("Alice", self.mc.getLastWriteAccessByValue())
        self.assertRaises(PermissionError, self.mc.writeValue, 0xFF, "Bob")

        # Read test must make sure that it can be read and written to
        if not self.mc.canWrite():
            self.mc.toggleWrite("Alice")
        if not self.mc.canRead():
            self.mc.toggleRead("Bob")
            self.assertEqual("Bob", self.mc.getLastWriteAccessByValue())
        self.mc.writeValue(0xF, "Bob")
        value = self.mc.readValue()
        self.assertEqual(value, 0xF)

        # Read blocking test, make sure we can't read
        if self.mc.canRead():
            self.mc.toggleRead("Alice")
        self.assertRaises(PermissionError, self.mc.readValue)

        # Execute test, must make sure we can write and execute
        if not self.mc.canWrite():
            self.mc.toggleWrite("Bob")
        if not self.mc.canExecute():
            self.mc.toggleExecute("Alice")
            self.assertEqual("Alice", self.mc.getLastWriteAccessByValue())
        self.mc.writeValue(0xF, "Alice")
        value = self.mc.executeValue()
        self.assertEqual(value, 0xF)

        # Execute blocking test, make sure we can't execute
        if self.mc.canExecute():
            self.mc.toggleExecute("Bob")
            self.assertEqual("Bob", self.mc.getLastWriteAccessByValue())
        self.assertRaises(PermissionError, self.mc.executeValue)

    def test_canRead(self):
        """
        Validates good working of the canRead method for MemoryCell
        """
        self.assertEqual(bool(self.mc._permission & 0b100), self.mc.canRead())

    def test_toggleRead(self):
        """
        Validates good working of the toggleRead method for MemoryCell
        """
        if not self.mc.canRead():
            self.mc.toggleRead("Bob")
            self.assertEqual("Bob", self.mc.getLastWriteAccessByValue())
        self.assertEqual(True, self.mc.canRead())
        self.mc.toggleRead("Alice")
        self.assertEqual("Alice", self.mc.getLastWriteAccessByValue())
        self.assertEqual(False, self.mc.canRead())
        self.assertRaises(ValueError, self.mc.toggleWrite, b"Bob")

    def test_canWrite(self):
        """
        Validates good working of the canWrite method for MemoryCell
        """
        self.assertEqual(bool(self.mc._permission & 0b010), self.mc.canWrite())

    def test_toggleWrite(self):
        """
        Validates good working of the toggleWrite method for MemoryCell
        """
        if not self.mc.canWrite():
            self.mc.toggleWrite("Bob")
            self.assertEqual("Bob", self.mc.getLastWriteAccessByValue())
        self.assertEqual(True, self.mc.canWrite())
        self.mc.toggleWrite("Alice")
        self.assertEqual("Alice", self.mc.getLastWriteAccessByValue())
        self.assertEqual(False, self.mc.canWrite())
        self.assertRaises(ValueError, self.mc.toggleWrite, b"Bob")

    def test_canExecute(self):
        """
        Validates good working of the canExecute method for MemoryCell
        """
        self.assertEqual(bool(self.mc._permission & 0b001), self.mc.canExecute())

    def test_toggleExecute(self):
        """
        Validates good working of the toggleExecute method for MemoryCell
        """
        if not self.mc.canExecute():
            self.mc.toggleExecute("Bob")
            self.assertEqual("Bob", self.mc.getLastWriteAccessByValue())
        self.assertEqual(True, self.mc.canExecute())
        self.mc.toggleExecute("Alice")
        self.assertEqual("Alice", self.mc.getLastWriteAccessByValue())
        self.assertEqual(False, self.mc.canExecute())
        self.assertRaises(ValueError, self.mc.toggleExecute, b"Bob")

    def test_getLastWriteAccessByValue(self):
        """
        Validates good working of the getLastWriteAccessByValue method for MemoryCell
        """
        mc = None
        mc = MemoryCell()
        self.assertEqual(mc.getLastWriteAccessByValue(), "System")
        mc.toggleExecute("Execute")
        self.assertEqual("Execute", mc.getLastWriteAccessByValue())
        mc.toggleExecute("Read")
        self.assertEqual("Read", mc.getLastWriteAccessByValue())
        mc.toggleExecute("Write")
        self.assertEqual("Write", mc.getLastWriteAccessByValue())

        if not mc.canWrite():
            mc.toggleWrite("Write")
        mc.writeValue(0xFF, "WriteValue")
        self.assertEqual("WriteValue", mc.getLastWriteAccessByValue())


if __name__ == '__main__':
    unittest.main()