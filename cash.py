import time
import sys
from cash.fs import fs

#Setup:
#   all the functions at the top, then cash function which opens the virt-fs, starts the main loop and refreshes the fs every loop
#   otherwise, the cash function works very similarly to the main catconsole program. will likely replace CatConsole's default cl

global file
global context
# the file object is currently always global, and the fs-lines array will remain local to each individual function. this is so that functions can edit their respective lines array without affecting other functions, as those changes won't take effect until they are truly written to the file

def cd(name):   #
    global context
    lines = file.readlines()
    file.seek(0)

    here = lines[context - 1]   #basically equal to the line of the fs we're currently in
    hereitems = here.split(",") #array of all the individual components of the current directory

    #see if the command is asking to "cd ..", in which case context is switched to the directory's parent dir (assuming context != root)
    if name == "..":
        if hereitems[0].split(":")[2] != "":
            context = int(hereitems[0].split(":")[2])
            return
        else:
            return

    #make sure the target directory exists
    herels = ret_ls()
    if name not in herels:
        print("No directory named \"" + name + "\"")
        return

    #create array of all the child-objects of the current directory; find which one matches the target directory; make sure the target directory is actually a directory, if so then change context to match
    dir_list = []
    n = 0
    targetID = 0
    for i in hereitems:
        if n != 0:
            dir_list.append(lines[int(i) - 1])
            if lines[int(i) - 1].split(",")[0].split(":")[1] == name:
                targetID= int(i)
            #break
        n = n + 1
    n = 0
    #print(dir_list, targetID)
    for i in dir_list:
        if dir_list[n].split(",")[0].split(":")[1] == name.strip():
            #print("AAAAAA")
            if dir_list[n].split(",")[0].split(":")[0] != "1":
                print("Not a directory")
                return
            else:
                #print("WAWAWAWA")
                context = targetID
                return
        n = n + 1
    print("Something went wrong...")
    return 1

def ret_ls():   #returns an array of all the names of the child objects of context
    lines = file.readlines()
    file.seek(0)
    here = lines[context-1]     #basically equal to the line of the fs we're currently in
    hereitems = here.split(",") #array of all the individual components of the current directory

    #adds every child object to an array, then makes an array out of just the names of all the child objects (and returns it)
    ls_list = []
    dir_list = []               #note: this name is kinda inaccurate since it actually stores any/every of context's child objects, not just the directories
    n = 0
    for i in hereitems:
        if n != 0:
            dir_list.append(lines[int(i) - 1])
            #print(dir_list, n, i)
        n = n + 1
    #print(dir_list, " <-dir_list")
    n = 0
    for i in dir_list:
        dirname = dir_list[n].split(",")[0].split(":")[1] #for each number in dir_list, go to that line, go to first area before a comma, and go to second area between colons (ie where the name of each child object can be found)
        ls_list.append(dirname)
        n = n + 1
    return ls_list

def ls():   #literally just uses ret_ls() and then outputs to console as one string lol
    local_ret_ls = ret_ls()
    localls = ""
    for i in local_ret_ls:
        localls = localls + i + " "
    print(localls)
    return

def create_child(lines):
    # looking for closest space available to write/overwrite new directory, modifying population array as appropriate
    n = 0
    dirID = n  # dirID will be in array form (ie if the file line is 5, the notation would be [4]; basically [X + 1])
    reconstruct = ""
    usingBlankSpace = False
    # print(len(lines[2].strip())) #<--this is the length of the POPULATION ARRAY!!! NOT lines!!!
    for item in lines[2].strip():
        if int(item) == 0 and usingBlankSpace == False:
            usingBlankSpace = True  # goes thru list of ones & zeroes, converts the first zero it gets to into a 1
            reconstruct += "1"
            dirID = n
        else:
            reconstruct += item
        n = n + 1
    if usingBlankSpace == True:
        lines[2] = reconstruct + "\n"
    else:
        dirID = n
        reconstruct += "1"
        lines[2] = reconstruct + "\n"
        lines.append("")

    lines[context - 1] = lines[context - 1].strip() + "," + str(dirID + 1) + "\n"

    return [lines, dirID]

def mkdir(name):    #assuming the new dir name is valid and available: locates closest free fs line on population array (if any, otherwise just adds to it), uses that line for new dir, and adds line# to current dir and makes dir at that line
    lines = file.readlines()
    file.seek(0)

    # checking that directory can be created
    if ":" in name or "/" in name or "," in name or "\n" in name or " " in name:
        print("Invalid name: cannot contain spaces, \":\", \",\", \"/\", or \"\\n\"")
        return
    allnames = ret_ls()
    for i in allnames:
        if i == name:
            print("That name already exists")
            return

    create_childOutput = create_child(lines)
    lines = create_childOutput[0]
    dirID = create_childOutput[1]

    lines[dirID] = "1:" + name + ":" + str(context) + "\n"
    #print(lines)
    file.writelines(lines)
    file.seek(0)
    return

def rmdir(name):
    lines = file.readlines()
    file.seek(0)

    # checking that directory exists and is valid. assuming it is, execution continues in if block
    if ":" in name or "/" in name or "," in name or "\n" in name or " " in name:
        print("Invalid name: cannot contain spaces, \":\", \",\", \"/\", or \"\\n\"")
        return
    allnames = ret_ls()
    nameexists = False
    for i in allnames:
        if i == name:
            nameexists = True
    if nameexists:

        #checking context subdir by subdir to find which one matches name
        n = 0
        dirID = 0
        foundID = False #contingency, realistically there's no reason we shouldn't find the ID if nameexists == True
        for i in lines[context-1].split(","):
            if n != 0:
                if lines[int(i) - 1].split(",")[0].split(":")[1] == name:
                    dirID = int(i)
                    foundID = True
            n = n + 1

        #just in case; this SHOULD never happen though, right?? :)
        if foundID != True:
            print("An unexpected error has occurred. Please go cry in a corner as necessary.")
            return

        #make sure object is a directory, and that it has no child directories of its own

        if lines[dirID - 1].strip().split(",")[0].split(":")[0] == "1":
            n = 0
            for i in lines[dirID - 1].strip().split(","):
                n = n + 1
            if n > 1:
                print("Error: \"" + name + "\" is not empty.")
                return
        else:
            print("\"" + name +"\": not a directory")
            return

        #delete data at dirID
        lines[dirID - 1] = "\n"

        #remove name's entry from context (aaaaaaaaaa)
        rebuildcontext = ""
        working_rebuildcontext = ""
        skip = False
        commacount = 0
        n = 0
        for char in lines[context - 1].strip():     #working_rebuildcontext           #dude. im not even gonna lie. you're gonna have to figure this for block out on your own. it barely works as it is, i don't even wanna waste time documenting it because im 90% sure imma end up needing to change it later anyways
            if working_rebuildcontext == str(dirID) and char == ",":
                skip = True
            else:
                skip = False

            if char == "," and skip == False:
                if commacount == 0:
                    rebuildcontext = rebuildcontext + working_rebuildcontext
                    working_rebuildcontext = ""
                    commacount = commacount + 1
                else:
                    rebuildcontext = rebuildcontext + "," + working_rebuildcontext
                    working_rebuildcontext = ""
                    commacount = commacount + 1
            elif char == "," and skip == True:
                working_rebuildcontext = ""
                skip = False
            elif char != "," and skip == False:
                working_rebuildcontext = working_rebuildcontext + char
            else:
                print("Uh Oh! The thing that wasn't supposed to happen just happened!")
                return

            if len(lines[context - 1].strip()) == n + 1 and working_rebuildcontext != str(dirID):
                rebuildcontext = rebuildcontext + "," + working_rebuildcontext
                working_rebuildcontext = ""
            n = n + 1
            #print(rebuildcontext, working_rebuildcontext, skip, char)
        lines[context - 1] = rebuildcontext + "\n"  #actually do the thing now
        print(lines, rebuildcontext)

        #clear newly freed space from the population array
        n = 0
        rebuild_poparray = ""
        for bit in lines[2].strip():
            if n == (dirID - 1):
                if int(bit) == 1:
                    rebuild_poparray = rebuild_poparray + "0"
                else:
                    print("How unfortunate. An error has occurred. You should probably go check that")  #lets hope this never happens
                    return
            else:
                rebuild_poparray = rebuild_poparray + bit
            n = n + 1
        lines[2] = rebuild_poparray + "\n"
        print(lines)

        #write to file.
        file.writelines(lines)
        file.seek(0)

        #(end of if block, natural return
    else:
        print("No such name: \"" + name + "\"")
        return
    return

class File:
    def __init__(self):
        self.get_context = lambda: globals().get("context") #THEORETICALLY, should set "get context" as a lambda function that returns the updated value every time it gets called
        self.context = self.get_context()
        self.get_lines = lambda: self._getLines()   #should call below function,
        self.lines = self.get_lines()

    def _getLines(self):    #for use in self.get_lines()
        return
#        get_file = lambda: globals().get("file")
#        f = get_file()
#        lines = f.readlines()
#        get_file().seek(0)
#        return lines

    def writeLines(self, lines):    #for any situation needing to write to file, may need to be expanded on to write only specific lines (seek(line), writeline(), seek(0))
        get_file = lambda: globals().get("file")
        get_file().writelines(lines)
        get_file().seek(0)
        return

    def checkIfFile(self):
        self.context = self.get_context()
        self.lines = self.get_lines()
        if self.lines[self.context - 1].split(",")[0].split(":")[0] == "2":
            return True
        else:
            return False

    def encodeData(self, string):
        reconstruction = ""
        for letter in string:
            if letter == "\\":
                reconstruction = reconstruction + "\\\\"
            elif letter == "\n":
                reconstruction = reconstruction + "\\n"
            elif letter == ":":
                reconstruction = reconstruction + "\\:"
            else:
                reconstruction = reconstruction + letter
        return reconstruction

    def decodeData(self, string):
        reconstruction = ""
        last2letters = []
        letterCount = 0
        for letter in string:
            if letterCount < 2:
                last2letters.append(letter)
                letterCount = letterCount + 1
            elif letterCount == 2:
                if last2letters[0] != "\\":
                    reconstruction = reconstruction + last2letters[0]
                    last2letters[0] = last2letters.pop()
                    letterCount = letterCount - 1
                else:
                    if last2letters[1] == "\\":
                        reconstruction = reconstruction + "\\"
                        last2letters.remove(1)
                        last2letters.remove(0)
                        letterCount = 0
                    elif last2letters[1] == "n":
                        reconstruction = reconstruction + "\n"
                        last2letters.remove(1)
                        last2letters.remove(0)
                        letterCount = 0
                    elif last2letters[1] == ":":
                        reconstruction = reconstruction + ":"
                        last2letters.remove(1)
                        last2letters.remove(0)
                        letterCount = 0
                    else:
                        reconstruction = reconstruction + last2letters[0] + last2letters[1]
                        last2letters.remove(1)
                        last2letters.remove(0)
                        letterCount = 0
                last2letters.append(letter)
                letterCount = letterCount + 1
            else:
                print("ruh roh")
                return
        return reconstruction

    def newFileInLines(self, name):
        self.context = self.get_context()
        self.lines = self.get_lines()
        newlinesAndDir = create_child(self.lines)
        self.lines = newlinesAndDir[0]
        dirID = newlinesAndDir[1]
        self.lines[dirID] = "2:" + str(name) + ":" + str(context) + "::"
        return self.lines

    def retFileData(self):
        pass

fileOp = File()

def test_func():
    return

def cash():
    global context
    global file
    ensure_exists = open("testing.txt", "a")
    ensure_exists.close()
    with open("testing.txt", "r+") as fs:
        file = fs
        fslines = fs.readlines()
        fs.seek(0)
        #print(lines)
        if len(fslines) < 1 or (len(fslines) > 2 and fslines[1].strip() != "0"):
            initFS()
            fslines = fs.readlines()
            fs.seek(0)
            print(fslines, "!!!!!!")
        context = int(fslines[0])      #context will always need to be converted to array form
        #ls()
        #cd("george")
        #ls()
        #cd("pinky")
        while True:
            #check if root, start building current path
            fslines = fs.readlines()
            fs.seek(0)
            currentpath = []
            tracecontext = context
            cashpath = ""
            traced = False
            while not traced:
                #print(fslines[tracecontext - 1].split(",")[0].split(":")[0])
                if fslines[tracecontext - 1].split(",")[0].split(":")[0] != "0":
                    currentpath.append(fslines[tracecontext - 1].split(",")[0].split(":")[1])
                    tracecontext = int(fslines[tracecontext - 1].split(",")[0].split(":")[2])
                if fslines[tracecontext - 1].split(",")[0].split(":")[0] == "0":
                    traced = True
                    currentpath.append("/")
                    break
                currentpath.append("/")
            #print(tracecontext, currentpath)
            if len(currentpath) < 2:
                cashpath = currentpath[0]
            else:
                for i in currentpath[::-1]: #reverse of array for loop
                    cashpath = cashpath + i
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
                    rmdir(cashcat.split(" ")[1])

            elif cashcat.split(" ")[0] == "cd":
                if len(cashcat.split(" ")) > 2:
                    print("cd: too many arguments")
                elif len(cashcat.split(" ")) < 2:
                    print("cd: too few arguments")
                else:
                    cd(cashcat.split(" ")[1])

            elif cashcat == "ls":
                ls()

            elif cashcat.split(" ")[0] == "mkdir":
                if len(cashcat.split(" ")) > 2:
                    print("mkdir: too many arguments")
                elif len(cashcat.split(" ")) < 2:
                    print("mkdir: too few arguments")
                else:
                    mkdir(cashcat.split(" ")[1])

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
                with open("consoleopener.txt", "r+") as f:
                    f.write(input("  >:"))
            else:
                print('"' + cashcat + '" is not a recognised command')













