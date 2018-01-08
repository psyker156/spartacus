![Spartacus Logo](Images/spartacus-logo.jpg)
# Spartacus Quick Start
## Dependencies
Spartacus relies on:

* python 3
* python 3 tkinter

Please install these before anything else.

## First Step
Create a virtual hard drive file using the following command:
> python3 HardDriveCreator.py -o HD.bin

If everything went well, the following text should be displayed on the terminal:
```
Hard drive creation about to begin, following options will be used
  output file:            HD.bin
Hard drive creation done, output file has been written to HD.bin 
```

Copy the testFiles/Hello.casm to the root of the project.
Use this command to assemble the Hello.casm file:
>python3 Assembler.py -i Hello.casm -o Hello.o

Validate that no error message are present on the output of the assembler.
The output should look like:
```
Assembler about to begin, following options will be used
  input file:             Hello.casm
  output file:            Hello.o
Assembler done, output file has been written to Hello.o
```

If everything went well, you can now use the following command to link the resulting file:
>python3 Linker.py -i Hello.o -o Hello.bin

Validate that no error message are present on the output of the linker.
The output should look like:
``` 
Linker about to begin, following options will be used
  input file:             ['Hello.o']
  symbols file:           Hello.sym
  output file:            Hello.bin
Linker done, output file has been written to Hello.bin
```

If everything went well, you can now use the following command to launch the debugger with the Hello.bin file:
>python3 Debugger.py -i Hello.bin

If the debugger was successfully launched, a black window should have appeared. Also, the debugger should have printed
the following information on the terminal:
``` 
Debug session about to begin, following options will be used
  input file:             Hello.bin
  symbols file:             Hello.sym
Building Capua execution environment
Loading ('Hello.bin',) in memory
Done loading ('Hello.bin',) into memory
Loading symbols from file Hello.sym
Done loading symbols
Debugging session is ready to be used. Have fun!

Next instruction to be executed:
0x40000000 : MOV #0x40000071 $S 
('Hello.bin',):
```

If everything went well, you can put a breakpoint on the endless loop. To do so, you can use the 
following command:
>break Hello.ENDLESSLOOP

Following which you can type the following command:
>continue

If you followed all direction, the message "Hello World!" should be displayed in the virtual display (the black window)

You can now type the following at the command line:
>quit

If you're here and the message is displayed, everything is working! Congratulations, you have a working Capua environment!

- - -
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