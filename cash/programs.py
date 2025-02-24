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

def copy_file(name, destination):
    global context
    preserveContext = []
    preserveContext.append(context)
    if name not in fs.dir.ret_ls():
        print("No such file: \"" + name + "\" not found")
        return 1
    if fs.file.ret_object_type_by_name(name) != 2:
        print("Error: attempting to copy file, but object is not a file")
        return 1
    fileData = fs.file.ret_file_data_from_name(name)
    if not isinstance(fileData, str):
        print("Cannot proceed with operation")
        return 1
    processing = ""
    currentDirID = context
    for char in destination:
        if char == "/":
            if processing == "..":
                currentDirID = fs.dir.ret_cd("..", currentDirID)
                processing = ""
                if currentDirID == -1:
                    print("Cannot proceed with operation")
                    return 1
            else:
                currentDirID = fs.dir.ret_cd(processing, currentDirID)
                processing = ""
                if currentDirID == -1:
                    print("Cannot proceed with operation")
                    return 1
        else:
            processing = processing + char
    context = currentDirID
    testMkFile = fs.file.mkfile(name)
    if testMkFile != 0:
        print("Cannot proceed with operation")
        return 1
    testWriteData = fs.file.write_file_data_from_name(fileData, name)
    if testWriteData != 0:
        print("Cannot proceed with operation")
        return 1
    context = preserveContext[0]
    return 0

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
    referenceVarToMakeSureWeDontLoopForever = []
    def print_help_str(thingToPrint, commandName):
        print("  " + rColored.lB(commandName) + ":")  # prints the command name
        n = 0
        for line in thingToPrint.split("\n"):
            if n < 1:
                print(rColored.gray(line))
            else:
                print(rColored.gray(" " + line))
        return 0

    def parse_help_str(commandName):
        if commandName in dictionary.keys():
            if len(dictionary[commandName][2]) > 0:  # if the help string isn't empty
                if dictionary[commandName][2][0] != "*":  # if the first letter of the help string equals something other than "*"
                    print_help_str(dictionary[commandName][2], commandName)
                elif len(dictionary[commandName][2]) > 1:  # if the first letter of the help string equals "*" and the help string has more than one char
                    if dictionary[commandName][2][1] != "*":  # if the second letter of the help string equals something other than "*"
                        n = 0
                        correctedHelpString = ""
                        while n < len(dictionary[commandName][2]):
                            if n == 0:
                                n = 1
                            else:
                                correctedHelpString = correctedHelpString + dictionary[commandName][2][n]
                                n = n + 1
                        print_help_str(correctedHelpString, commandName)
                    else:#if the first two letters are "**"
                        n = 0
                        referencedCommandName = ""
                        while n < len(dictionary[commandName][2]):
                            if n < 2:
                                n = 2
                            else:
                                referencedCommandName = referencedCommandName + dictionary[commandName][2][n]
                                n = n + 1
                        if referencedCommandName.lower().strip() in dictionary.keys():
                            if referencedCommandName in referenceVarToMakeSureWeDontLoopForever:
                                print("Invalid reference: command \"" + commandName + "\" causes reference loop in help")
                                return 2
                            else:
                                referenceVarToMakeSureWeDontLoopForever.append(referencedCommandName)
                                recursiveExecution = parse_help_str(referencedCommandName)
                                if isinstance(recursiveExecution, bool):
                                    if not recursiveExecution:
                                        print(args[0][0][0] + ": References nonexistant command")
                                elif isinstance(recursiveExecution, int):
                                    if recursiveExecution == 0:
                                        return 0
                                    elif recursiveExecution == 1:
                                        return 1
                                    else:
                                        return 1
                                else:
                                    return None
                        else:
                            print("Invalid reference: command references command \"" + referencedCommandName + "\", however no such command can be found")
                            return 1
                else:
                    print("No help data available")  # i know this can be made better, but idc
                    return 1
            else:
                print("No help data available")
                return 1
        else:
            return False
        return 0

    if len(args[0][0]) > 0:# if command was passed with arguments?
        argumentOne= args[0][0][0].lower()
        if len(args[0][0]) > 1:
            print("help: Too many arguments")
            return 1
        else:
            parsedHelp = parse_help_str(argumentOne)
            if isinstance(parsedHelp, bool):
                if not parsedHelp:
                    print(args[0][0][0] + ": No such command")
            elif isinstance(parsedHelp, int):
                if parsedHelp == 0:
                    return 0
                elif parsedHelp == 1:
                    return 1
                else:
                    print("\"help " + argumentOne + "\": There was an unknown error in help. This is ungood.")
                    return 1
            else:
                print("There was an unknown error in help. This is ungood.")
                return 1
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
    print("Enter desired data to be written.\nAfter entering data, type \"QQ\" to quit and write to file, or type \"QQ\" now to leave file untouched")
    data = ""
    n = 0
    userEndedSession = False
    while not userEndedSession:
        prompt = input().strip()
        if prompt == "QQ":
            if n > 0:
                userEndedSession = True
            else:
                return 0
        else:
            if n > 0:
                data = data + "\n" + prompt
            else:
                data = data + prompt
        n = n + 1
        return 1

def mv(*args):
    def mv_file(name, destination):

        testCP = copy_file(name, destination)
        return 0

    def mv_dir(name, destination):
        print("not used yet")
        return 0

    if len(args[0][0]) == 1:
        if args[0][0].lower() == "file" or args[0][0].lower() == "f":
            print("Enter file name:")
            ls()
            fName = input(">:")
            if fName not in fs.dir.ret_ls():
                print("No such file: \"" + fName + "\" not found")
                return 1
            dName = input("Enter destination name:\n>:")
            mv_file(fName, dName)
        elif args[0][0].lower() == "folder" or args[0][0].lower() == "directory" or args[0][0].lower() == "dir" or args[0][0].lower() == "d":
            print("Enter directory name:")
            ls()
            fName = input(">:")
            if fName not in fs.dir.ret_ls():
                print("No such directory: \"" + fName + "\" not found")
                return 1
            dName = input("Enter destination directory:\n>:")
            mv_dir(fName, dName)
        elif args[0][0] in fs.dir.ret_ls():
            dName = input("Enter destination directory:\n>:")
            if fs.file.check_if_file(fs.file.ret_objectID(args[0][0])):
                mv_file(args[0][0], dName)
            elif fs.dir.check_if_dir(fs.file.ret_objectID(args[0][0])):
                mv_dir(args[0][0], dName)
            else:
                print("Error: object of unknown type")
                return 1
        else:
            print("Bad input: \"" + args[0][0] + "\" is not valid input")
            return 1
    elif len(args[0]) == 2:
        if args[0][0].lower() == "file" or args[0][0].lower() == "f":
            if args[0][1].lower() in fs.dir.ret_ls():
                if not fs.file.check_if_file(fs.file.ret_objectID(args[0][1])):
                    print("Error: \"" + args[0][1] + "\" is not a file")
                    return 1
                dName = input("Enter destination directory:\n>:")
                mv_file(args[0][1], dName)
        elif args[0][0].lower() == "folder" or args[0][0].lower() == "directory" or args[0][0].lower() == "dir" or args[0][0].lower() == "d":
            if args[0][1].lower() in fs.dir.ret_ls():
                if not fs.dir.check_if_dir(fs.file.ret_objectID(args[0][1])):
                    print("Error: \"" + args[0][1] + "\" is not a directory")
                    return 1
                dName = input("Enter destination directory:\n>:")
                mv_dir(args[0][1], dName)
        elif args[0][0].lower() in fs.dir.ret_ls():
            if fs.file.check_if_file(fs.file.ret_objectID(args[0][0])):
                mv_file(args[0][0], args[0][1])
            elif fs.dir.check_if_dir(fs.file.ret_objectID(args[0][0])):
                mv_dir(args[0][0], args[0][1])
            else:
                print("Error: object of unknown type")
                return 1
        else:
            print("Bad input: \"" + args[0][0] + "\" is not valid input")
            return 1
    elif len(args[0]) == 3:
        if args[0][0].lower() == "file" or args[0][0].lower() == "f":
            if args[0][1].lower() in fs.dir.ret_ls():
                if not fs.file.check_if_file(fs.file.ret_objectID(args[0][1])):
                    print("Error: \"" + args[0][1] + "\" is not a file")
                    return 1
                mv_file(args[0][1], args[0][2])
        elif args[0][0].lower() == "folder" or args[0][0].lower() == "directory" or args[0][0].lower() == "dir" or args[0][0].lower() == "d":
            if args[0][1].lower() in fs.dir.ret_ls():
                if not fs.dir.check_if_dir(fs.file.ret_objectID(args[0][1])):
                    print("Error: \"" + args[0][1] + "\" is not a directory")
                    return 1
                mv_dir(args[0][1], args[0][2])
        elif args[0][0].lower() in fs.dir.ret_ls():
            if fs.file.check_if_file(fs.file.ret_objectID(args[0][0])):
                mv_file(args[0][0], args[0][1])
            elif fs.dir.check_if_dir(fs.file.ret_objectID(args[0][0])):
                mv_dir(args[0][0], args[0][1])
            else:
                print("Error: object of unknown type")
                return 1
        else:
            print("Bad input: \"" + args[0][0] + "\" is not valid input")
            return 1
    elif len(args[0]) > 3:
        print("Error: too much input")
    else:
        print("What would you like to move? (file, directory)")
        inp = input(">:")
        if inp.lower() == "file" or inp.lower() == "f":
            print("Enter file name:")
            ls()
            fName = input(">:")
            if fName not in fs.dir.ret_ls():
                print(fName + ": Not found")
                return 1
            if not fs.file.check_if_file(fs.file.ret_objectID(fName)):
                print("Error: \"" + fName + "\" is not a file")
                return 1
            dName = input("Enter destination name:\n>:")
            mv_file(fName, dName)
        elif inp.lower() == "folder" or inp.lower() == "directory" or inp.lower() == "dir" or inp.lower() == "d":
            print("Enter directory name:")
            ls()
            fName = input(">:")
            if fName not in fs.dir.ret_ls():
                print(fName + ": Not found")
                return 1
            if not fs.dir.check_if_dir(fs.file.ret_objectID(fName)):
                print("Error: \"" + fName + "\" is not a directory")
                return 1
            dName = input("Enter destination directory:\n>:")
            mv_dir(fName, dName)
        elif inp in fs.dir.ret_ls():
            dName = input("Enter destination directory:\n>:")
            if fs.file.check_if_file(fs.file.ret_objectID(inp)):
                mv_file(args[0][0], inp)
            elif fs.dir.check_if_dir(fs.file.ret_objectID(inp)):
                mv_dir(args[0][0], inp)
            else:
                print("Error: object of unknown type")
                return 1
        else:
            print("Bad input: \"" + inp + "\" is not valid input")
            return 1




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
    "move": [lambda *args: mv(args), -1, "Command to move files/directories\nDoes not require static amount of arguments"],
    "jaguar": [lambda arg: jaguar(arg), 1, "*"],
    "jag": [lambda arg: jaguar(arg), 1, "**jaguar"],
}
