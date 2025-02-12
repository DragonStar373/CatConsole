import sys
import time
from cash import cash, help_func
from carmode import carmode
from REPEATINGCAT import rcat
from nyan import nyanfunction
global mazeImported
try:
    from maze.mazik import mazik
    mazeImported = True
except ImportError:
    mazeImported = False
#at some point there will be a custom beginning file that the user can permanantly change, requires changing and reading text files

#opener = "consoleopener.txt"
#with open(opener) as nameillneveruseagain:
#    startmsg = nameillneveruseagain.read()
#print(startmsg)

#Setup:
#   Imports all subprograms, takes variable "fox" as input, and compares it to a list of all commands
#
global context

builtin = {
    "carmode": [lambda: carmode(), 0, ""],
    "car": [lambda: carmode(), 0, ""],
    "nyan": [lambda: nyanfunction(), 0, ""],
    "rcat": [lambda: rcat(), 0, ""],
    "repeatingcat": [lambda: rcat(), 0, ""],
    "help": [lambda: help_func(builtin), 0, ""]
}
if mazeImported:
    builtin["maze"] = [lambda: mazik(), 0, ""]

while True:
    cashret = cash()
    if cashret != 0:
        if cashret.lower().split(" ")[0] in builtin:
            if (len(cashret.lower().split(" ")) - 1) > builtin[cashret.lower().split(" ")[0]][1]:
                print(str(cashret.lower().split(" ")[0]) + ": Too many arguments")
            elif (len(cashret.lower().split(" ")) - 1) < builtin[cashret.lower().split(" ")[0]][1]:
                print(str(cashret.lower().split(" ")[0]) + ": Too few arguments")
            else:
                commandargs = []
                execcommand = "builtin[cashret.lower().split(" ")[0]][0]("
                n = 0
                for i in range(1, len(cashret.lower().split(
                        " "))):  # no need for the -1, because we need that extra number anyways
                    commandargs.append(cashret.lower().split(" ")[i])
                for arg in commandargs:
                    if n == 0:
                        execcommand = execcommand + "\"" + arg + "\""
                    else:
                        execcommand = execcommand + ", " + "\"" + arg + "\""
                    n = n + 1
                execcommand = execcommand + ")"
                exec(execcommand)
        
print("Goodbye")