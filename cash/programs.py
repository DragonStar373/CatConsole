from .fs import fs
import sys, os

global context


class PrintColors:

    def __init__(self):
        pass

    def rBG(skk): print("\033[41m {}\033[00m".format(skk))

    def gBG(skk): print("\033[42m {}\033[00m".format(skk))

    def bBG(skk): print("\033[44m {}\033[00m".format(skk))

    def yBG(skk): print("\033[43m {}\033[00m".format(skk))

    def mBG(skk): print("\033[45m {}\033[00m".format(skk))

    def cBG(skk): print("\033[46m {}\033[00m".format(skk))

    def blackBG(skk): print("\033[40m {}\033[00m".format(skk))

    def gray(skk): print("\033[37m {}\033[00m".format(skk))

    def grayBG(skk): print("\033[47m {}\033[00m".format(skk))

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


def ls():       #in the future: make it accept arguments, such as for listing order or for only listing certain items

    def default_assembly(itemList, count):
        locStringToPrint = ""
        n = 1

        if count == 0 or count is None or not count:
            for i in itemList:
                locStringToPrint = locStringToPrint + i + " "
            return locStringToPrint

        for i in itemList:
            if n >= count + 1:
                n = 0
                locStringToPrint = locStringToPrint + "\n" + i + " "
            else:
                if n == count:
                    locStringToPrint = locStringToPrint + i
                else:
                    locStringToPrint = locStringToPrint + i + " "
            n = n + 1
        return locStringToPrint

    def assembly_with_console(itemList, retLs, count):#assumes itemList and retLs have equal lengths; requires both because the color tags tend to skew how long a word will actually be
        currentLine = ""
        currentUncoloredLine = ""
        finalString = ""
        currentList = []
        n = 0
        while True:
            #to treat as if part of a for loop; an actual for loop is not feasible as we must iterate over both the colored and uncolored items
            if n >= len(itemList):
                break
            i = itemList[n]
            # make sure that at any point, if an item won't fit, it abandons everything and just does the default
            if len(i) >= consoleWidth:
                finalString = default_assembly(itemList, count)
                currentLine = ""
                break
            #iteration
            if len(currentUncoloredLine + retLs[n] + " ") < consoleWidth and len(currentList) < count:  # if it fits and is less than / equal to count:
                currentLine = currentLine + i + " "
                currentUncoloredLine = currentUncoloredLine + retLs[n] + " "
                currentList.append(i)
            elif len(currentUncoloredLine + retLs[n]) > consoleWidth or len(currentList) >= (count):  # if the reduced version doesn't fit or is more than count:
                currentLine = currentLine + "\n" + i
                finalString = finalString + currentLine
                currentLine = ""
                currentUncoloredLine = ""
                currentList = []
            else:  # if the reduced version does fit and the line is less than / equal to count
                currentLine = currentLine + i + "\n"
                finalString = finalString + currentLine
                currentLine = ""
                currentUncoloredLine = ""
                currentList = []
            n = n + 1

        if currentLine != "":  # in case the last working line never got added to the final string
            finalString = finalString + currentLine
        return finalString

    lsOutput = fs.dir.ret_ls()
    lsList = []

    #reformats the default ret_ls() output with colors and spaces
    for i in lsOutput:
        if fs.file.ret_object_type_by_name(i) == 1:
            lsList.append(rColored.lC(i))
        elif fs.file.ret_object_type_by_name(i) == 2:
            lsList.append(rColored.lG(i))
        else:
            lsList.append(rColored.lR(i))

    #attempts to get current terminal width, with a fallback in place if it throws an exception
    try:
        consoleWidth = os.get_terminal_size().columns
        divByColumn = True
    except OSError:
        consoleWidth = 0
        divByColumn = False
    #formats arrangement so that each line never exceeds the width of the console or the total max item count per amount of items; falls back to a default method if any single item is ever too big or if console width could not be determined
    stringToPrint = ""
    if divByColumn:
        if len(lsList) < 31:
            stringToPrint = assembly_with_console(lsList, lsOutput, 8)
        elif len(lsList) < 43:
            stringToPrint = assembly_with_console(lsList, lsOutput, 10)
        else:
            stringToPrint = assembly_with_console(lsList, lsOutput, 16)
    else:
        stringToPrint = default_assembly(lsList, 10)




    print(stringToPrint)
    return 0

def help_func(dictionary, *args):
    if len(args[0][0]) > 0:# if command was passed with arguments?
        argumentOne = args[0][0][0].lower()
        if len(args[0][0]) > 1:
            print("help: Too many arguments")
            return 1
        else:
            if argumentOne in dictionary.keys():
                if len(dictionary[argumentOne][2]) > 0:#if the help string isn't empty
                    if dictionary[argumentOne][2][0] != "*":#if the first letter of the help string equals something other than "*"
                        print("  " + rColored.lB(argumentOne) + ":")#prints the command name
                        n = 0
                        for line in dictionary[argumentOne][2].split("\n"):
                            if n < 1:
                                print(rColored.gray(line))
                            else:
                                print(rColored.gray(" " + line))
                    elif len(dictionary[argumentOne][2]) > 1:
                        if dictionary[argumentOne][2][1] != "*":
                            n = 0
                            correctedHelpString = ""
                            while n < len(dictionary[argumentOne][2]):
                                if n == 0:
                                    n = 1
                                else:
                                    correctedHelpString = correctedHelpString + dictionary[argumentOne][2][n]
                                    n = n + 1
                            print("  " + rColored.lB(argumentOne) + ":")
                            n = 0
                            for line in correctedHelpString.split("\n"):
                                if n < 1:
                                    print(rColored.gray(line))
                                else:
                                    print(rColored.gray(" " + line))
                        else:
                            print("Command references another command; however, this functionality has not yet been expanded on because I am lazy. Too bad, very sad.")
                    else:
                        print("No help data available")#i know this can be made better, but idc
                else:
                    print("No help data available")
            else:
                print(args[0][0][0] + ": No such command")
    else:
        fullHelpString = ""
        listHeader = ""
        n = 0
        for name in dictionary.keys():
            helpString = dictionary[name][2]
            if name == "DictName":
                if len(dictionary[name]) >= 4:
                    listHeader = dictionary[name][3]
                    n = n - 1
            elif len(helpString) > 0:
                if helpString[0] != '*':
                    if n > 0:
                        fullHelpString = fullHelpString + ("\n" + "  " + name)
                    else:
                        fullHelpString = fullHelpString + ("  " + name)
            else:
                if n > 0:
                    fullHelpString = fullHelpString + ("\n" + "  " + name)
                else:
                    fullHelpString = fullHelpString + ("  " + name)
            n = n + 1
        if listHeader != "":
            print(listHeader)
        print(fullHelpString)
        print("Use \"help {command}\" for more information")

        return 0

def test_func():
    return

def jaguar(filename):
    return











global progs
#after the *, hidden commands either A: contain the help string for that command or B: contain another * followed by the name of a command whose help string should be referenced
# noinspection PyRedeclaration
progs = {           #structure= key:[function, argument count, help string(haven't done yet)];      if argument count == -1 (or any negative value), program takes any number of operators;     if help string starts with "*", do not display in help menu
    "DictName": [lambda: exec("break"), 0, "*", "System Commands"],
    "quit": [lambda: sys.exit(), 0, "Command used to close CatConsole\nTakes no arguments"],
    "exit": [lambda: sys.exit(), 0, "**quit"],
    "help": [lambda *args: help_func(progs, args), -1, "This is the help command!"],
    "cd": [lambda arg: fs.dir.cd(arg), 1, "Command used to change directory (ie. move to a new folder)\nTarget directory must located in current directory; use the `ls` command to view items in current directory\nPass `..` as an argument to back out of current directory\nRequires one argument: `cd {directory_name}`"],
    "ls": [lambda: ls(), 0, "Command used to list all items in the current directory\nListed items are colorcoded, with directories shown in cyan and files shown in green\nTakes no arguments"],
    "mkdir": [lambda arg: fs.dir.mkdir(arg), 1, "Command used to create a new directory/folder inside of the current one\nNew directory name cannot be \".\", \"..\", or a duplicate of another item in the current directory\nRequires one argument: `mkdir {directory_name}`"],
    "rmdir": [lambda arg: fs.dir.rmdir(arg), 1, "Command used to remove a directory\nTarget directory must be located in current directory and must be empty\nRequires one argument: `rmdir {directory_name}`"],
    "testfunc": [lambda: test_func(), 0, "*Function for internal testing"],
    "rm": [lambda arg: fs.file.rmfile(arg), 1, "Command used to remove a file\nTarget file must be located in current directory\nRequires one argument: `rm {file_name}`"],
    "del": [lambda arg: fs.file.rmfile(arg), 1, "**rm"],
    "touch": [lambda arg: fs.file.mkfile(arg), 1, "**mkfile"],
    "mkfile": [lambda arg: fs.file.mkfile(arg), 1, "Command used to create a new file inside of the current directory\nFile name cannot be \".\", \"..\", or a duplicate of another item in the current directory\nRequires one argument: `mkfile {file_name}`"],
    "echo": [lambda  arg: print(fs.file.ret_file_data_from_name(arg)), 1, "Command used to echo the contents of a file (ie. display the file's data)\nRequires one argument: `echo {file_name}`"],
    "edit": [lambda arg: fs.file.edit_file(arg), 1, ""],
    "jaguar": [lambda arg: jaguar(arg), 1, "*"],
    "jag": [lambda arg: jaguar(arg), 1, "**jaguar"],
}
