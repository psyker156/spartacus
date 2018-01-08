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
from Configuration.Configuration import INTERRUPT_CLOCK

import threading
import time

__author__ = "CSE"
__copyright__ = "Copyright 2017, CSE"
__credits__ = ["CSE"]
__license__ = "GPL"
__version__ = "2.0"
__maintainer__ = "CSE"
__status__ = "Dev"


class InterruptClock(BaseDevice):
    """
    This device is a Clock that will generate interrupts on a given time interval.
    This type of device is required in order to allow for multiprogramming.
    The first 4 bytes of the memory reserved for this device holds the timer value in milliseconds.
    """

    def __init__(self, parentMIOC=None):
        super(InterruptClock, self).__init__(parentMIOC=parentMIOC)
        self._data = b"\x00" * 0xFF
        self.startAddress = 0x20000300
        self.mask = 0xFFFFFF00
        self._interruptGenerator = True
        self._interruptNumber = INTERRUPT_CLOCK
        self._timerLength = 0.0
        self._timerRunning = False
        self._clockThread = threading.Thread(target=self._runClock)

    def _memoryAction(self, source=None):
        """
        This will simply set the timer interval after a write had been made. It will also start the timer if
        it's not currently running.
        :param source:
        :return:
        """
        interval = self._readFromDataBuffer(offset=0, length=4)
        self._setTimer(interval)

        if not self._timerRunning:
            self._startTimer()

    def _setTimer(self, timerLength=0):
        """
        This method is meant to be used for direct manipulation of the timer value.
        :param timerLength: int, this is a value representing the number of milliseconds the timer will wait
        :return: Nothing is returned
        """
        self._timerLength = float(timerLength) / 1000

    def _startTimer(self):
        """
        This will launch the thread that allows the timer to work in a separated thread
        :return:
        """
        self._clockThread.start()

    def _runClock(self):
        """
        This is an endless loop that will sleep for a certain time and then generate
        an interrupt to be handled by the execution unit.
        :return:
        """
        self._timerRunning = True

        while True:
            if self._shutdownProcedureInAction:
                # This allows the method to return if we need to shutdown the system
                break
            time.sleep(self._timerLength)
            self._parentMIOC.eu.signalHardwareInterrupt(self._interruptNumber)
