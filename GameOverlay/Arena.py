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
__version__ = "1.3"
__maintainer__ = "CSE"
__status__ = "Dev"


class Arena:
    """
    This is nothing more than a "helper" class that aims at displaying the game state.
    """
    def __init__(self):
        # colorama.init()
        pass

    def displayFirstInterface(self, p1, p2):
        print("")
        print("----------------------------------------------------------------------")
        print("                                                                      ")
        print("                                                                      ")
        print("                                                                      ")
        print("                                                                      ")
        print("                                                                      ")
        print("                                                                      ")
        print("                                                                      ")
        print("                                                                      ")
        print("                  Welcome to Spartacus Code battle!                   ")
        print("                  Virtual machine is now initializing                 ")
        print("                  Contestants are being feed...                       ")
        print("                                                                      ")
        print("                    {} vs. {}".format(p1, p2,))
        print("                                                                      ")
        print("                  Battle is about to begin...                         ")
        print("                                                                      ")
        print("                                                                      ")
        print("                                                                      ")
        print("                                                                      ")
        print("                                                                      ")
        print("                                                                      ")
        print("----------------------------------------------------------------------")
        print("")


    def displayGameState(self, p1capua=None, p2capua=None):

        print("")
        print("")
        print("Current Memory Map")
        print("----------------------------------------------------------------------")

        # Here we need to print memory status!
        # 16 lines, 64 unit per line, 1024 bytes per unit

        p1Count = 0
        p2Count = 0
        for byte in range(1, (16 * 64 * 1024) + 1):

            if p1capua.eu.mioc._memoryArray._memoryCellArray[byte-1]._lastWriteAccessBy == p1capua.eu.name:
                p1Count += 1
            elif p2capua.eu.mioc._memoryArray._memoryCellArray[byte-1]._lastWriteAccessBy == p2capua.eu.name:
                p2Count += 1

            if byte % 1024 == 0:
                # We need to write a unit to the screen
                char = " "
                if p1Count > p2Count:
                    char = "@"
                elif p2Count > p1Count:
                    char = "*"

                print(char, end="")
                # Reset count for next unit
                p1Count = 0
                p2Count = 0

            if (byte / 1024) % 64 == 0 and byte != 0:
                # We need to write a line
                print("\n", end="")

        print("----------------------------------------------------------------------")
        print("{}  @".format(p1capua.eu.name,))
        print("{}  *".format(p2capua.eu.name,))
        print("----------------------------------------------------------------------")
        print("")

    def displayGameStop(self, message=""):
        print("")
        print("----------------------------------------------------------------------")
        print("()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()")
        print("()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()")
        print(message)
        print("()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()")
        print("()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()")
        print("----------------------------------------------------------------------")
        print("")

    def displayContextCrash(self, message="", contextDump=None):
        print("")
        print("----------------------------------------------------------------------")
        print("()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()")
        print("()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()")
        print(message)
        print("Crashed thread context information dump:")
        print(str(contextDump))
        print("()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()")
        print("()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()")
        print("----------------------------------------------------------------------")
        print("")
