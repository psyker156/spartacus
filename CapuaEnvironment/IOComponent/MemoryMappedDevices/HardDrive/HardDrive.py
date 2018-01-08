#!/usr/bin/env python
#  -*- coding: <utf-8> -*-

"""
This file is part of Spartacus project
Copyright (C) 2017  CSE

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

from CapuaEnvironment.IOComponent.MemoryMappedDevices.BaseDevice import BaseDevice
from Configuration.Configuration import HARD_DRIVE_FILE_PATH, \
                                        HARD_DRIVE_MAX_SIZE, \
                                        HARD_DRIVE_SECTOR_SIZE, \
                                        INTERRUPT_HARD_DRIVE_DONE_READ,\
                                        INTERRUPT_HARD_DRIVE_DONE_WRITE


import mmap
import struct
import threading
import time

__author__ = "CSE"
__copyright__ = "Copyright 2017, CSE"
__credits__ = ["CSE"]
__license__ = "GPL"
__version__ = "2.0"
__maintainer__ = "CSE"
__status__ = "Dev"


class HardDrive(BaseDevice):
    """
    This device is a virtual hard drive
    """

    def __init__(self, parentMIOC=None):
        super(HardDrive, self).__init__(parentMIOC=parentMIOC)
        self._data = b"\x00" * 0xFF
        self.startAddress = 0x20000400
        self.mask = 0xFFFFFF00

        self._hdLock = threading.Lock()

        self._hdFile = open(HARD_DRIVE_FILE_PATH, "r+b")
        self._hdMmap = mmap.mmap(fileno=self._hdFile.fileno(), length=0)     # Map the whole file

        self._watchDogThread = threading.Thread(target=self._hdWatchDog)
        self._watchDogThread.start()

    def _hdWatchDog(self):
        """
        This method is running within a thread. This will watch for the shutdown notice and
        close file handle and memory map if required.
        :return: Nothing
        """
        while not self._shutdownProcedureInAction:
            time.sleep(2)
        self._hdMmap.close()
        self._hdFile.close()

    def _memoryAction(self, source="System"):
        """
        This only happens after a write. If an action should be taken, the action will be taken here
        In the case of the current device, the only possible actions are read or write from/to disk

        0x20000400 = 0x0 for a read operation or 0x01 for a write operation
        0x20000404 = LBA to be written or read
        0x20000408 = Memory Address to write TO or to read FROM
        0x2000040C = Trigger memory action = When this is set to 1, the action is triggered

        :param source: String, who is at the origin of this action
        :return:
        """
        trigger = self._readFromDataBuffer(offset=0xC, length=4)
        if trigger != 1:
            return

        operation = self._readFromDataBuffer(offset=0, length=4)
        lba = self._readFromDataBuffer(offset=4, length=4)
        bufferAddress = self._readFromDataBuffer(offset=8, length=4)

        if operation == 0:
            # This is a read operation
            readThread = threading.Thread(target=self._readDisk, args=(lba, bufferAddress,))
            readThread.start()
        elif operation == 1:
            # This is a write operation
            writeThread = threading.Thread(target=self._writeDisk, args=(lba, bufferAddress,))
            writeThread.start()
        else:
            # This is invalid.
            raise RuntimeError("Invalid hard drive operation code. 1=write, 0=read, else is error")

    def _readDisk(self, lba=None, destBuffer=None):
        """
        This method will read a specified LBA from the disk and copy it at the specified address.
        When done, it will generate the appropriate interrupt on the core.
        :param lba: int, a number indicating the number of the block to be read
        :param destBuffer: the address of the buffer where the LBA needs to be written in memory
        :return: Nothing
        """

        startLocation = lba*HARD_DRIVE_SECTOR_SIZE

        self._hdLock.acquire()
        lbaData = self._hdMmap[startLocation:startLocation+HARD_DRIVE_SECTOR_SIZE]

        # Read from the data present in the LBA and copy to memory
        for i in range(0, HARD_DRIVE_SECTOR_SIZE, 4):
            toBeWrittenInMemory = struct.unpack(">I", lbaData[startLocation:startLocation + 4])[0]
            self._parentMIOC.memoryWriteAtAddressForLength(address=destBuffer, length=4, value=toBeWrittenInMemory)
            startLocation += 4  # Reaching next block of memory
            destBuffer += 4     # Reaching next block of memory
        # Only thing left is signaling the interrupt. No need to hug the lock from here
        self._hdLock.release()

        signaled = False
        while not signaled:
            signaled = self._parentMIOC.eu.signalHardwareInterrupt(INTERRUPT_HARD_DRIVE_DONE_READ)
        return

    def _writeDisk(self, lba=None, srcBuffer=None):
        """
        This method will write data from a specified address (sourceBuffer) to a given LBA on the disk
        :param lba: int, a number indicating the number of the block to be written
        :param srcBuffer: the address of the buffer where the information is to be read
        :return: Nothing
        """
        startLocation = lba*HARD_DRIVE_SECTOR_SIZE

        self._hdLock.acquire()

        for i in range(startLocation, startLocation + HARD_DRIVE_SECTOR_SIZE, 4):
            toBeWrittenOnDisk = self._parentMIOC.memoryReadAtAddressForLength(address=srcBuffer, length=4)
            readyBytes = struct.pack(">I", toBeWrittenOnDisk)
            self._hdMmap[startLocation] = readyBytes[0]
            self._hdMmap[startLocation + 1] = readyBytes[1]
            self._hdMmap[startLocation + 2] = readyBytes[2]
            self._hdMmap[startLocation + 3] = readyBytes[3]
            startLocation += 4
            srcBuffer += 4
        # Only thing left is signaling the interrupt. No need to hug the lock from here
        self._hdLock.release()

        signaled = False
        while not signaled:
            signaled = self._parentMIOC.eu.signalHardwareInterrupt(INTERRUPT_HARD_DRIVE_DONE_WRITE)

        return
