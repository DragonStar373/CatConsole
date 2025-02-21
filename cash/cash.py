import time
import sys
from .fs import fs
from .programs import progs
#Setup:
#   all the functions at the top, then cash function which opens the virt-fs, starts the main loop and refreshes the fs every loop
#   otherwise, the cash function works very similarly to the main catconsole program. will likely replace CatConsole's default cl

global context
# the file object is currently always global, and the fs-lines array will remain local to each individual function. this is so that functions can edit their respective lines array without affecting other functions, as those changes won't take effect until they are truly written to the file



def cash():
    global context
    #check if root, start building current path
    cashpath = fs.dir.ret_path_at_context()

    cashcat = input("" + cashpath + " >$")


    if cashcat.lower().split(" ")[0] in progs:
        #determining if the program has a set amount of operators or not
        if progs[cashcat.lower().split(" ")[0]][1] < 0:
            commandargs = []
            execcommand = "progs[cashcat.lower().split(" ")[0]][0](["
            #creates list of all the arguments posed after the command
            for i in range(1, len(cashcat.lower().split(" "))):  # no need for the -1, because we need that extra number anyways
                commandargs.append(cashcat.split(" ")[i])
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
        #assuming the program does in fact have a set amount of operators, these if statements ensures that amount is met before running the command
        elif (len(cashcat.lower().split(" ")) - 1) > progs[cashcat.lower().split(" ")[0]][1]:
            print(str(cashcat.lower().split(" ")[0]) + ": Too many arguments")
            return 1
        elif (len(cashcat.lower().split(" ")) - 1) < progs[cashcat.lower().split(" ")[0]][1]:
            print(str(cashcat.lower().split(" ")[0]) + ": Too few arguments")
            return 1
        else:
            commandargs = []
            execcommand = "progs[cashcat.lower().split(" ")[0]][0]("
            n = 0
            for i in range(1, len(cashcat.lower().split(" "))):     #no need for the -1, because we need that extra number anyways
                commandargs.append(cashcat.split(" ")[i])
            for arg in commandargs:
                if n == 0:
                    execcommand = execcommand + "\"" + arg + "\""
                else:
                    execcommand = execcommand + ", " + "\"" + arg + "\""
                n = n + 1
            execcommand = execcommand + ")"
            #print(execcommand)
            exec(execcommand)

        #if cashcat.lower().split(" ")[0] == "help":
        #    return cashcat.lower().split(" ")[0]
        return 0
    else:
        return cashcat














