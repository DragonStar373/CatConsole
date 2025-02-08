import time
import sys
from .fs import FS
fs = FS("testing.txt")

#Setup:
#   all the functions at the top, then cash function which opens the virt-fs, starts the main loop and refreshes the fs every loop
#   otherwise, the cash function works very similarly to the main catconsole program. will likely replace CatConsole's default cl

global context
# the file object is currently always global, and the fs-lines array will remain local to each individual function. this is so that functions can edit their respective lines array without affecting other functions, as those changes won't take effect until they are truly written to the file

def test_func():
    return

def cash():
    global context
    while True:
        #check if root, start building current path
        cashpath = fs.dir.trace_path()
        #print(cashpath)
        #main loop
        cashcat = input(""+ cashpath + " >$")
        if cashcat == "quit":
            sys.exit()
        elif cashcat == "cc":
            break
        elif cashcat == "help":
            print("Cash Commands:\n  cd {dir}\n  ls\n  mkdir {name}\nPublic Commands:\n  help\n  cc\n  maze\n  nyan\n  rcat\n  car\n  quit")

        elif cashcat.split(" ")[0] == "rmdir":
            if len(cashcat.split(" ")) > 2:
                print("rmdir: too many arguments")
            elif len(cashcat.split(" ")) < 2:
                print("rmdir: too few arguments")
            else:
                fs.dir.rmdir(cashcat.split(" ")[1])

        elif cashcat.split(" ")[0] == "cd":
            if len(cashcat.split(" ")) > 2:
                print("cd: too many arguments")
            elif len(cashcat.split(" ")) < 2:
                print("cd: too few arguments")
            else:
                fs.dir.cd(cashcat.split(" ")[1])

        elif cashcat == "ls":
            fs.dir.ls()

        elif cashcat.split(" ")[0] == "tap":
            if len(cashcat.split(" ")) > 2:
                print("tap: too many arguments")
            elif len(cashcat.split(" ")) < 2:
                print("tap: too few arguments")
            else:
                fs.file.mkfile(cashcat.split(" ")[1])

        elif cashcat.split(" ")[0] == "mkdir":
            if len(cashcat.split(" ")) > 2:
                print("mkdir: too many arguments")
            elif len(cashcat.split(" ")) < 2:
                print("mkdir: too few arguments")
            else:
                fs.dir.mkdir(cashcat.split(" ")[1])

        elif cashcat.split(" ")[0] == "python" or cashcat.split(" ")[0] == "py" or cashcat.split(" ")[0] == "python3":
            if len(cashcat.split(" ")) < 2:
                print(cashcat.split(" ")[0] +": too few arguments")
            else:
                if cashcat.split(" ")[1] == "print":
                    if len(cashcat.split(" ")) < 3:
                        print("print: too few arguments")
                    elif len(cashcat.split(" ")) > 3:
                        print("print: too many arguments")
                    else:
                        if cashcat.split(" ")[2] in globals():
                            print(globals()[cashcat.split(" ")[2]])
                        elif cashcat.split(" ")[2] in locals():
                            print(locals()[cashcat.split(" ")[2]])
                        else:
                            print("No known variables named \"" + cashcat.split(" ")[2] + "\"")
                            print(globals())
                            print(locals())
                elif cashcat.split(" ")[1] == "test_func()" or cashcat.split(" ")[1] == "test_func":
                    if len(cashcat.split(" ")) > 2:
                        print("print: too many arguments")
                    else:
                        test_funcExitCode = test_func()
                        print("Returned with \"" + str(test_funcExitCode) + "\"")
                else:
                    print("\"" + cashcat.split(" ")[1] + "\" is not a recognized command, or more likely has not been integrated")

        elif cashcat == "car":
            #carmode()
            pass
        elif cashcat == "cash":
            cash()
        elif cashcat == "nyan":
            pass
            #from nyan import nyanfunction
            #nyanfunction()
        elif cashcat == "maze":
            #from mazik.mazik import mazik
            print("make sure you run catconsole with 'python catconsole.py'")
            #mazik()
        elif cashcat.lower() == "rcat" or cashcat.lower() == "repeatingcat":
            #rcat()
            pass
        elif cashcat == "":
            pass
        elif cashcat.lower() == "motd":
            with open("../consoleopener.txt", "r+") as f:
                f.write(input("  >:"))
        else:
            print('"' + cashcat + '" is not a recognised command')













