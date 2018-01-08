![Spartacus Logo](Images/spartacus-logo.jpg)
# Guide de démarrage rapide de spartacus
## Dépendances
Spartacus dépend sur:

* python 3
* python 3 tkinter

Veuillez les installer avant de poursuivre.

## Première étape
Créer un fichier de disque rigide virtuel à l'aide de la commande suivante:
> python3 HardDriveCreator.py -o HD.bin

Si tout a bien fonctionné, le texte suivant devrait être affiché à la console:
```
Hard drive creation about to begin, following options will be used
  output file:            HD.bin
Hard drive creation done, output file has been written to HD.bin 
```

Copier le fichier testFiles/Hello.casm vers la racine du projet.
Utiliser cette commande afin d'assembler le fichier Hello.casm:
>python3 Assembler.py -i Hello.casm -o Hello.o

Valider qu'aucun message d'erreur n'est présent à la sortie de l'assembleur.
Le message de sortie de l'assembleur devrait ressembler à ceci:
```
Assembler about to begin, following options will be used
  input file:             Hello.casm
  output file:            Hello.o
Assembler done, output file has been written to Hello.o
```

Si tout s'est bien passé, vous pouvez maintenant utiliser la commande suivante afin de procéder
à l'édition des liens sur le fichier résultant de la commande précédente:
>python3 Linker.py -i Hello.o -o Hello.bin

Valider qu'aucun message d'erreur n'est présent à la sortie de l'éditeur de liens.
Le message de sortie de l'éditeur de liens devrait ressembler à ceci:
``` 
Linker about to begin, following options will be used
  input file:             ['Hello.o']
  symbols file:           Hello.sym
  output file:            Hello.bin
Linker done, output file has been written to Hello.bin
```

Si tout s'est bien passé, vous pouvez maintenant utiliser la commande suivante afin de lancer le débogueur avec
le fichier Hello.bin:
>python3 Debugger.py -i Hello.bin

Si le débogueur a été lancé avec succès, une fenêtre noire devrait apparaître.
Le debogueur devrait aussi afficher ceci sur la console:
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

Si tout a bien fonctionné, vous pouvez mettre un point d'arrêt sur la boucle sans fin. 
Pour se faire, vous pouvez utiliser la commande suivante:
>break Hello.ENDLESSLOOP

Suivant laquelle vous pouvez tapper la commande suivante:
>continue

Si vous avez suivi toutes les étape, le message "Hello World!" devrait être affiché à l'écran virtuelle (la fenêtre noire)

À la ligne de commande, vous pouvez maintenant faire la commande suivante:
>quit

Si vous êtes ici et que le message est affiché, tout fonctionne! Félicitations, vous avez un environnement Capua fonctionnel!

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
