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

from CapuaEnvironment.ExecutionUnit.ExecutionUnit import ExecutionUnit
from CapuaEnvironment.IntructionFetchUnit.InstructionFetchUnit import InstructionFetchUnit
from CapuaEnvironment.IOComponent.MemoryIOController import MemoryIOController
from CapuaEnvironment.MemoryArray.MemoryArray import MemoryArray

__author__ = "CSE"
__copyright__ = "Copyright 2015, CSE"
__credits__ = ["CSE"]
__license__ = "GPL"
__version__ = "2.1"
__maintainer__ = "CSE"
__status__ = "Dev"


class Capua:
    """
    This is the heart of the whole system. This is the glue that is holding all of CapuaEnvironment
    devices together.
    """

    ma = None
    mioc = None
    ifu = None
    eu = None

    def __init__(self, name="System"):
        """
        Preparing the whole execution environment for this Capua instance. Note that a single memory
        array can be shared between multiple Capua environment.
        """
        self.eu = ExecutionUnit(name)

        self.ma = MemoryArray()
        self.mioc = MemoryIOController(self.ma, testOnly=False)
        self.mioc.eu = self.eu
        self.ifu = InstructionFetchUnit(self.mioc, self.eu)

        self.eu.mioc = self.mioc
        self.eu.ifu = self.ifu




