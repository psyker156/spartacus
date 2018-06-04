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
__version__ = "2.2"
__maintainer__ = "CSE"
__status__ = "Dev"


MEMORY_START_AT = 0x40000000
MEMORY_ARRAY_NUMBER_OF_MEMORY_CELL = 0x100000 * 16  # 1 048 576 * 16 memory cells = 16 Megs of RAM
MEMORY_END_AT = MEMORY_START_AT + MEMORY_ARRAY_NUMBER_OF_MEMORY_CELL
MEMORY_CELL_INITIAL_VALUE = 0XFF  # NOP operation
MEMORY_MAXIMUM_READ_WRITE_SIZE = 0x04   # Maximum memory access operation size is 4 bytes

REGISTER_A = 0b0000
REGISTER_B = 0b0001
REGISTER_C = 0b0010
REGISTER_D = 0b0011
REGISTER_E = 0b0100
REGISTER_F = 0b0101
REGISTER_G = 0b0110

REGISTER_S = 0b0111

REGISTER_A2 = 0b1000
REGISTER_B2 = 0b1001
REGISTER_C2 = 0b1010
REGISTER_D2 = 0b1011
REGISTER_E2 = 0b1100
REGISTER_F2 = 0b1101
REGISTER_G2 = 0b1110

REGISTER_S2 = 0b1111

DISPLAY_REFRESH_RATE = 5      # This is in milliseconds
DISPLAY_FONT_SIZE = 12

KEYBOARD_REFRESH_RATE = 5      # This is in milliseconds
KEYBOARD_BUFFER_SIZE = 20       # How big is the keyboard buffer (scan code buffer)

HARD_DRIVE_FILE_PATH = "HD.bin"
HARD_DRIVE_SECTOR_SIZE = 512
HARD_DRIVE_MAX_SIZE = 2048    # Size is given in sectors!!! 2048 sectors of 512 bytes each = 1MB

INTERRUPT_CLOCK = 0x00
INTERRUPT_KEYBOARD = 0x01
INTERRUPT_HARD_DRIVE_DONE_READ = 0x02
INTERRUPT_HARD_DRIVE_DONE_WRITE = 0x03
EXCEPTION_BAD_INSTRUCTION_FETCH = 0x20
EXCEPTION_NO_EXECUTE_PERMISSION = 0x21
EXCEPTION_PAGE_NOT_AVAILABLE = 0x22
EXCEPTION_MEMORY_ACCESS_DENIED = 0x23
EXCEPTION_DIVIDE_BY_ZERO = 0x24
EXCEPTION_EXECUTION_PRIVILEGE_VIOLATION = 0x25

DEBUGGER_WAKEUP_TICK_COUNT = 0    # Used to keep debugger "in control"

VIRTUAL_BOOT_ENABLED = True       # This will enforce booting from the "hard drive" by using the "firmware"
FIRMWARE_LOAD_ADDRESS = 0x40001000      # Firmware will be loaded at this address when using virtual boot
FIRMWARE_BINARY_FILE_PATH = "CapuaEnvironment/firmware.bin"

VIRTUAL_PAGE_MASK = 0xFFFFFFFF & (0b1111111111111 << 19)
VIRTUAL_ADDRESS_MASK = VIRTUAL_PAGE_MASK ^ 0xFFFFFFFF
VIRTUAL_TABLE_ENTRY_MASK = 0b1111111111111
VIRTUAL_EXECUTABLE_FLAG = 0b1000000000000000
VIRTUAL_PRIVILEGED_FLAG = 0b0100000000000000
VIRTUAL_AVAILABLE_FLAG = 0b0010000000000000
VIRTUAL_NULL = 0

ACCESS_GRANTED = 0

