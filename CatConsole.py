import time

from carmode import carmode
from REPEATINGCAT import rcat
from spec.spec import spec
from ConsoleManager import manager
#from maze.mazik import mazik
#at some point there will be a custom beginning file that the user can permanantly change, requires changing and reading text files

opener = "consoleopener.txt"
with open(opener) as nameillneveruseagain:
    startmsg = nameillneveruseagain.read()


print(startmsg)

while True:
    fox = input(">:")
    if fox == "quit" or fox == "exit":
        break
    elif fox == "help":
        print("Public Commands:\n  help\n  maze\n  nyan\n  rcat\n  car\n  quit\n  spec")
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
    elif fox.lower() == "motd":
        print("still working on this!")
    elif fox.lower() == "spec":
        spec()
    elif fox.lower() == "manager-pc":
        manager("Prog/Com")
    else:
        print('"' + fox + '" is not a recognised command')
        
print("Goodbye")