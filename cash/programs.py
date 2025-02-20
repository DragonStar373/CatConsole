from logging import exception

from numpy.f2py.auxfuncs import throw_error

from .fs import fs
import sys, os

global context

class PrintColors:

    def __init__(self):
        pass

    def dR(skk): print("\033[41m {}\033[00m".format(skk))

    def dG(skk): print("\033[42m {}\033[00m".format(skk))

    def dB(skk): print("\033[44m {}\033[00m".format(skk))

    def dY(skk): print("\033[43m {}\033[00m".format(skk))

    def dM(skk): print("\033[45m {}\033[00m".format(skk))

    def dC(skk): print("\033[46m {}\033[00m".format(skk))

    def blackBG(skk): print("\033[40m {}\033[00m".format(skk))

    def white(skk): print("\033[37m {}\033[00m".format(skk))

    def lGray(skk): print("\033[47m {}\033[00m".format(skk))

    def black(skk): print("\033[30m {}\033[00m".format(skk))

    def lR(skk): print("\033[31m {}\033[00m".format(skk))

    def lG(skk): print("\033[32m {}\033[00m".format(skk))

    def lB(skk): print("\033[34m {}\033[00m".format(skk))

    def lY(skk): print("\033[33m {}\033[00m".format(skk))

    def lM(skk): print("\033[35m {}\033[00m".format(skk))

    def lC(skk): print("\033[36m {}\033[00m".format(skk))

class RetColors:

    def __init__(self):
        pass

    def rBG(skk): return "\033[41m {}\033[00m".format(skk)

    def gBG(skk): return "\033[42m {}\033[00m".format(skk)

    def bBG(skk): return "\033[44m {}\033[00m".format(skk)

    def yBG(skk): return "\033[43m {}\033[00m".format(skk)

    def mBG(skk): return "\033[45m {}\033[00m".format(skk)

    def cBG(skk): return "\033[46m {}\033[00m".format(skk)

    def blackBG(skk): return "\033[40m {}\033[00m".format(skk)

    def gray(skk): return "\033[37m {}\033[00m".format(skk)

    def grayBG(skk): return "\033[47m {}\033[00m".format(skk)

    def black(skk): return "\033[30m {}\033[00m".format(skk)

    def lR(skk): return "\033[31m {}\033[00m".format(skk)

    def lG(skk): return "\033[32m {}\033[00m".format(skk)

    def lB(skk): return "\033[34m {}\033[00m".format(skk)

    def lY(skk): return "\033[33m {}\033[00m".format(skk)

    def lM(skk): return "\033[35m {}\033[00m".format(skk)

    def lC(skk): return "\033[36m {}\033[00m".format(skk)

rColored = RetColors
pColored = PrintColors

#ls:
#no more than 6 per line UNLESS total number of items is more than 30 -- > 6x5 for listing items
#hard max of 8 per line
#recursively add items - if an item being added would clip the string in the console, don't add it and set that limit as the total row length limit -- requires getting console width
#if item# == 31 to 42: row length = 7; else, row length = max 8

#determine console width first, then separate into strings -- if any of the strings exceed console width, reduce row length and retry


def print_ls_line():
    pass

def ls():
    lsOutput = fs.dir.ret_ls()
    lsList = []

    for i in lsOutput:
        if fs.file.ret_object_type_by_name(i) == 1:
            lsList.append(rColored.lC(i + " "))
        elif fs.file.ret_object_type_by_name(i) == 2:
            lsList.append(rColored.lG(i + " "))
        else:
            lsList.append(rColored.lR(i + " "))

    divByColumn = False
    try:
        consoleWidth = os.get_terminal_size().columns
        divByColumn = True
    except OSError:
        consoleWidth = 0
        divByColumn = False



    stringToPrint = ""
    if len(lsList) < 5:
        if False:#replace false with "divByColumn" when ready
            pass
        else:
            n = 1
            for i in lsList:
                if n >= len(lsList):
                    stringToPrint = stringToPrint + i
                else:
                    stringToPrint = stringToPrint + i + " "
    elif len(lsList) < 10:
        if False:
            pass
        else:
            n = 1
            for i in lsList:
                if n < 6:
                    n = 0
                    stringToPrint = stringToPrint + "\n" + i + " "
                else:
                    if n >= len(lsList):
                        stringToPrint = stringToPrint + i
                    else:
                        stringToPrint = stringToPrint + i + " "

    else:
        pass



    print(stringToPrint)
    return 0

def help_func(dct):
    for name in dct.keys():
        print(" " + name)
    return 0

def test_func():
    return

def jaguar(filename):
    return











global progs
# noinspection PyRedeclaration
progs = {                   #structure= key:[function, argument count, help string(haven't done yet)]
    "quit": [lambda: sys.exit(), 0, ""],
    "exit": [lambda: sys.exit(), 0, ""],
    "cc": [lambda: exec("break"), 0, ""],
    "help": [lambda: help_func(progs), 0, ""],
    "cd": [lambda arg: fs.dir.cd(arg), 1, ""],
    "ls": [lambda: ls(), 0, ""],
    "mkdir": [lambda arg: fs.dir.mkdir(arg), 1, ""],
    "rmdir": [lambda arg: fs.dir.rmdir(arg), 1, ""],
    "testfunc": [lambda: test_func(), 0, ""],
    "rm": [lambda arg: fs.file.rmfile(arg), 1, ""],
    "del": [lambda arg: fs.file.rmfile(arg), 1, ""],
    "touch": [lambda arg: fs.file.mkfile(arg), 1, ""],
    "echo": [lambda  arg: print(fs.file.ret_file_data_from_name(arg)), 1, ""],
    "edit": [lambda arg: fs.file.edit_file(arg), 1, ""],
}

