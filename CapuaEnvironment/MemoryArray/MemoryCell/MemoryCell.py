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

__author__ = "CSE"
__copyright__ = "Copyright 2015, CSE"
__credits__ = ["CSE"]
__license__ = "GPL"
__version__ = "2.0"
__maintainer__ = "CSE"
__status__ = "Dev"


class MemoryCell:
    """
    MemoryCell represent a single memory cell inside of Capua execution environment.
    Those cells are grouped in a memory array to form the complete memory region
    to be used inside of Capua. Each cell is 1 byte wide
    """

    _permission = 0b000  # Permission are octal RWX
    _value = 0x00
    _lastWriteAccessBy = "System"

    def __init__(self, permission=0b100, value=0x00):
        """
        After construction, memory cell is ready to be integrated inside of a memory
        array.
        Permissions is a 3 bits field defined as:
            0b100 = Read
            0b010 = Write
            0b001 = Execute
        Value can be at max 0xFF since each memory cell have 1 byte of usable memory
        :param permission: Int, Permission to be applied to the cell
        :param value: Int, Cell initialisation value
        :return: None but raise exception if init fails
        """

        if 0b000 <= permission <= 0b111:
            self._permission = permission
        else:
            raise ValueError("Invalid permission given")

        if 0x0 <= value <= 0xFF:
            self._value = value
        else:
            raise ValueError("Invalid value given")

    def writeValue(self, value=0x00, accessedBy="System"):
        """
        This will write a value to the current cell
        :param value: A value to be written to this memory cell
        :param accessedBy: name of the system requiring access
        :return: Nothing
        """
        if not self.canWrite():
            raise PermissionError("Denied write access")

        if not 0x0 <= value <= 0xFF:
            raise ValueError("Invalid value given, too big or too small")

        if not type(accessedBy) is str:
            raise ValueError("Invalid accessor name must be string")

        self._lastWriteAccessBy = accessedBy
        self._value = value

    def readValue(self):
        """
        Returns the value of the cell if cell is in readable mode. Otherwise, exception is raised.
        :return: Numeric value of the cell
        """
        if not self.canRead():
            raise PermissionError("Denied read access")
        return self._value

    def executeValue(self):
        """
        Returns the value of the cell if cell is in an executable mode. Otherwise, exception is raised.
        :return: Numeric value of the cell
        """
        if not self.canExecute():
            raise PermissionError("Denied execute access")
        return self._value

    def canRead(self):
        """
        This will return True if the cell is in a readable state. Otherwise it return False
        """
        readable = 0b100 & self._permission
        return bool(readable)

    def toggleRead(self, accessedBy):
        """
        This will set the read bit permission for this cell
        :param accessedBy: name of the system requiring access
        """
        if not type(accessedBy) is str:
            raise ValueError("Invalid accessor name must be string")

        self._lastWriteAccessBy = accessedBy
        self._permission ^= 0b100

    def canWrite(self):
        """
        This will return True if the cell is in a writable state. Otherwise it return False
        """
        writable = 0b010 & self._permission
        return bool(writable)

    def toggleWrite(self, accessedBy):
        """
        This will set the write bit permission for this cell
        :param accessedBy: name of the system requiring access
        """
        if not type(accessedBy) is str:
            raise ValueError("Invalid accessor name must be string")

        self._lastWriteAccessBy = accessedBy
        self._permission ^= 0b010

    def canExecute(self):
        """
        This will return True if the cell is in an executable state. Otherwise it return False
        """
        executable = 0b001 & self._permission
        return bool(executable)

    def toggleExecute(self, accessedBy):
        """
        This will set the execute bit permission for this cell
        :param accessedBy: name of the system requiring access
        """
        if not type(accessedBy) is str:
            raise ValueError("Invalid accessor name must be string")

        self._lastWriteAccessBy = accessedBy
        self._permission ^= 0b001

    def getLastWriteAccessByValue(self):
        """
        Simply return the name of the last element that modified the memory cell
        Modification = change in value or change in permission
        :return: String representing the name of the last modificator
        """
        return self._lastWriteAccessBy
