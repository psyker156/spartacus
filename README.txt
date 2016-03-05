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


NOTE:
All documentation is available in the "Documentation" folder.
Please note that some code examples are available in the "testFiles"
folder. Also note, for those who like code coloring, a Notepad++
syntax file is available at "Documentation/CapuaASM-NPPLanguage.xml".
Simply import that file into your "user defined" language in NPP
in order to benefit from code coloring for the Capua assembly language.

The Assembler.py, Linker.py, Debugger.py and Game.py files are meant to
be used by the user. Simply invoque these from the command line in order
to be able to see how to use them. Help option = -h

About the folders:
CapuaEnvironment:
    This folder is where the VM code sits.
Configuration:
    This folder holds multiple configuration elements used at multiple place inside the project
Documentation:
    All non code documentation is in there
GameOverlay:
    This is where the game code is. Both for the interface and game management.
ToolChain:
    NOTE ABOUT THE TOOL CHAIN:
        This tool chain was originally built for testing purpose not for programmer.
        Therefore, bugs are present and code is NOT fully tested.
    All tool chain related code is here. For example, the code allowing to parse and link files
    is in there. The debugger code is there too.
testFiles:
    This directory holds multiple code example that were used while developing the Spartacus project.
