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

from Configuration.Configuration import HARD_DRIVE_SECTOR_SIZE, \
                                        HARD_DRIVE_MAX_SIZE

import argparse
import os

__author__ = "CSE"
__copyright__ = "Copyright 2017, CSE"
__credits__ = ["CSE"]
__license__ = "GPL"
__version__ = "2.0"
__maintainer__ = "CSE"
__status__ = "Dev"


def parseCommandLineArgs():
    """
    As implied by the name, this will parse the command line arguments so we can use them. Important note,
    after this function is called, no need to use the "extension" attribute since this one is concatenated
    with the "output". This results in cleaner code since those two are always(? most of the time at least)
    used together.
    :return: A parsed object as provided by argparse.parse_args()
    """
    parser = argparse.ArgumentParser(prog="HardDriveCreator.py",
                                     description="Capua Hard Drive Creator Version {}".format(__version__,),
                                     epilog="This tool is provided as part of Spartacus learning environment under {} "
                                            "licence. Feel free to distribute, modify, "
                                            "contribute and learn!".format(__license__,))

    parser.add_argument("-o", "--output",
                        required=True,
                        nargs=1,
                        type=str,
                        help="Define the output where the hard drive file is to be created")

    args = parser.parse_args()
    args.output = args.output[0]

    return args


def validatePaths(argsWithPaths):
    """
    This function will simply validate that the input path exists
    :param argsWithPaths: An input parsed object as provided by argparse.parse_args()
    :return: This does not return. Simply raises ValueError in cases where paths are not valid.
    """
    if os.path.exists(argsWithPaths.output):
        raise ValueError("ERROR: file {} already exists.".format(argsWithPaths.output,))


if __name__ == '__main__':
    usableArgs = parseCommandLineArgs()
    print(usableArgs)
    validatePaths(usableArgs)  # Make sure the parsed info is usable before using it!

    print("Hard drive creation about to begin, following options will be used")
    print("  output file:            {}".format(usableArgs.output,))

    f = open(usableArgs.output, "wb")
    for i in range(0, HARD_DRIVE_MAX_SIZE):
        f.write(b"\x00" * HARD_DRIVE_SECTOR_SIZE)
    f.close()

    if os.path.exists(usableArgs.output):
        # The assembler did the job correctly and the out file has been written to disk!
        print("Hard drive creation done, output file has been written to {}". format(usableArgs.output,))
