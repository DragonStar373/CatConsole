import time
from cash import cash
from carmode import carmode
from REPEATINGCAT import rcat
#from maze.mazik import mazik
#at some point there will be a custom beginning file that the user can permanantly change, requires changing and reading text files

#opener = "consoleopener.txt"
#with open(opener) as nameillneveruseagain:
#    startmsg = nameillneveruseagain.read()
#print(startmsg)

#Setup:
#   Imports all subprograms, takes variable "fox" as input, and compares it to a list of all commands
#
global context

while True:
    fox = input(">:")
    if fox == "quit":
        break
    elif fox == "help":
        print("Public Commands:\n  help\n  cash\n  maze\n  nyan\n  rcat\n  car\n  quit")
    elif fox == "cash":
        cash()
    elif fox == "car":
        carmode()
    elif fox == "nyan":
        from nyan import nyanfunction
        nyanfunction()
    elif fox == "maze":
        from mazik.mazik import mazik
        print("make sure you run catconsole with 'python catconsole.py'")
        mazik()
    elif fox.lower() == "rcat" or fox.lower() == "repeatingcat":
        rcat()
    elif fox == "":
        pass
    #elif fox.lower() == "motd":        tbd, might remove for permanent
    #    with open("consoleopener.txt", "r+") as f:
    #        f.write(input("  >:"))
    else:
        print('"' + fox + '" is not a recognised command')
        
print("Goodbye")