import sys
import time
from cash import cash, help_func
from carmode import carmode
from REPEATINGCAT import rcat
from nyan import nyanfunction
global context
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


builtin = {
    "carmode": [lambda: carmode(), 0, ""],
    "car": [lambda: carmode(), 0, ""],
    "nyan": [lambda: nyanfunction(), 0, ""],
    "rcat": [lambda: rcat(), 0, ""],
    "repeatingcat": [lambda: rcat(), 0, ""],
    "help": [lambda *args: help_func(builtin, args), -1, "This is the help command!"]
}
if mazeImported:
    builtin["maze"] = [lambda: mazik(), 0, ""]

while True:
    cashret = cash()
    if isinstance(cashret, str):
        if str(cashret).lower().split(" ")[0] in builtin:
            if builtin[cashret.lower().split(" ")[0]][1] < 0:
                commandargs = []
                execcommand = "builtin[cashret.lower().split(" ")[0]][0](["
                # creates list of all the arguments posed after the command
                for i in range(1, len(cashret.lower().split(" "))):  # no need for the -1, because we need that extra number anyways
                    commandargs.append(cashret.split(" ")[i])
                #
                n = 0
                for arg in commandargs:
                    if n == 0:
                        execcommand = execcommand + "\"" + arg + "\""
                    else:
                        execcommand = execcommand + ", " + "\"" + arg + "\""
                    n = n + 1
                execcommand = execcommand + "])"
                # print(execcommand)
                exec(execcommand)
            if (len(cashret.lower().split(" ")) - 1) > builtin[cashret.lower().split(" ")[0]][1]:
                print(str(cashret.lower().split(" ")[0]) + ": Too many arguments")
            elif (len(cashret.lower().split(" ")) - 1) < builtin[cashret.lower().split(" ")[0]][1]:
                print(str(cashret.lower().split(" ")[0]) + ": Too few arguments")
            else:
                commandargs = []
                execcommand = "builtin[cashret.lower().split(" ")[0]][0]("
                n = 0
                for i in range(1, len(cashret.lower().split(" "))):  # no need for the -1, because we need that extra number anyways
                    commandargs.append(cashret.lower().split(" ")[i])
                for arg in commandargs:
                    if n == 0:
                        execcommand = execcommand + "\"" + arg + "\""
                    else:
                        execcommand = execcommand + ", " + "\"" + arg + "\""
                    n = n + 1
                execcommand = execcommand + ")"
                exec(execcommand)
        else:
            print(str(cashret).lower().split(" ")[0] +": No such command")
    elif isinstance(cashret, int):
        if cashret == 1:
            finishedOnError = True
        elif cashret != 0:
            finishedOnError = True
            print("Unknown error in Cash")
        else:
            finishedOnError = False
print("Goodbye")