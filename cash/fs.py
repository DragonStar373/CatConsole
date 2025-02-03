import time
import sys

#from Xlib.ext.record import get_context

#Setup:
#   all the functions at the top, then cash function which opens the virt-fs, starts the main loop and refreshes the fs every loop
#   otherwise, the cash function works very similarly to the main catconsole program. will likely replace CatConsole's default cl

#global file
global context

class FSIO:
    global context

    def __int__(self, fileName):
        global context
        self.fileName = fileName
        self.lines = []
        ensure_exists = open(fileName, "a")
        ensure_exists.close()

        with open(fileName, "r+") as self.file:
            fs = self.file
            fsLines = fs.readlines()
            fs.seek(0)
            # print(lines)
            if len(fsLines) < 1 or (len(fsLines) > 2 and fsLines[1].strip() != "0"):
                self.initFS()
                self.lines = fs.readlines()
                fs.seek(0)
                print(fsLines, "!!!!!!")
            else:
                self.lines = fs.readlines()
                fs.seek(0)
            context = int(fsLines[0])

    def read_file(self):
        with open(self.fileName, "r+") as self.file:
            fsLines = self.file.readlines()
            self.file.seek(0)
        return fsLines

    def write_lines(self,lines):  # for any situation needing to write to file, may need to be expanded on to write only specific lines (seek(line), writeline(), seek(0))
        with open(self.fileName, "r+") as self.file:
            self.file.writelines(lines)
            self.file.seek(0)
        self.lines = self.read_file()
        return 0

    def ret_ls(self):  # returns an array of all the names of the child objects of context
        lines = self.read_file()
        here = lines[context - 1]  # basically equal to the line of the fs we're currently in
        hereitems = here.split(",")  # array of all the individual components of the current directory

        # adds every child object to an array, then makes an array out of just the names of all the child objects (and returns it)
        ls_list = []
        dir_list = []  # note: this name is kinda inaccurate since it actually stores any/every of context's child objects, not just the directories
        n = 0
        for i in hereitems:
            if n != 0:
                dir_list.append(lines[int(i) - 1])
                # print(dir_list, n, i)
            n = n + 1
        # print(dir_list, " <-dir_list")
        n = 0
        for i in dir_list:
            dirname = dir_list[n].split(",")[0].split(":")[
                1]  # for each number in dir_list, go to that line, go to first area before a comma, and go to second area between colons (ie where the name of each child object can be found)
            ls_list.append(dirname)
            n = n + 1
        return ls_list

    def init_FS(self):  # writes default base root fs format, circa revision 0. writes to file, then moves the file's pointer back to start again
        initarray = ["4\n", "0\n", "1111\n", "0:/::\n"]
        self.write_lines(initarray)
        self.lines = self.read_file()
        print(self.lines, "!!!!!!")
        return

    def mk_child_at_context(self):      #modifies self.lines, returns dirID of child object
        # looking for closest space available to write/overwrite new directory, modifying population array as appropriate
        n = 0
        dirID = n  # dirID will be in array form (ie if the file line is 5, the notation would be [4]; basically [X + 1])
        reconstruct = ""
        usingBlankSpace = False
        # print(len(lines[2].strip())) #<--this is the length of the POPULATION ARRAY!!! NOT lines!!!
        for item in self.lines[2].strip():
            if int(item) == 0 and usingBlankSpace == False:
                usingBlankSpace = True  # goes thru list of ones & zeroes, converts the first zero it gets to into a 1
                reconstruct += "1"
                dirID = n
            else:
                reconstruct += item
            n = n + 1
        if usingBlankSpace:
            self.lines[2] = reconstruct + "\n"
        else:
            dirID = n
            reconstruct += "1"
            self.lines[2] = reconstruct + "\n"
            self.lines.append("")

        self.lines[context - 1] = self.lines[context - 1].strip() + "," + str(dirID + 1) + "\n"   #add the child object to current dir

        return [dirID]

    def ret_ls_dirIDs(self):
        pass #maybe returns a dict? array? idk

#def cd(name):   #
#    global context
#    lines = file.readlines()
#    file.seek(0)
#
#    here = lines[context - 1]   #basically equal to the line of the fs we're currently in
#    hereitems = here.split(",") #array of all the individual components of the current directory
#
#    #see if the command is asking to "cd ..", in which case context is switched to the directory's parent dir (assuming context != root)
#    if name == "..":
#        if hereitems[0].split(":")[2] != "":
#            context = int(hereitems[0].split(":")[2])
#            return
#        else:
#            return
#
#    #make sure the target directory exists
#    herels = ret_ls()
#    if name not in herels:
#        print("No directory named \"" + name + "\"")
#        return
#
#    #create array of all the child-objects of the current directory; find which one matches the target directory; make sure the target directory is actually a directory, if so then change context to match
#    dir_list = []
#    n = 0
#    targetID = 0
#    for i in hereitems:
#        if n != 0:
#            dir_list.append(lines[int(i) - 1])
#            if lines[int(i) - 1].split(",")[0].split(":")[1] == name:
#                targetID= int(i)
#            #break
#        n = n + 1
#    n = 0
#    #print(dir_list, targetID)
#    for i in dir_list:
#        if dir_list[n].split(",")[0].split(":")[1] == name.strip():
#            #print("AAAAAA")
#            if dir_list[n].split(",")[0].split(":")[0] != "1":
#                print("Not a directory")
#                return
#            else:
#                #print("WAWAWAWA")
#                context = targetID
#                return
#        n = n + 1
#    print("Something went wrong...")
#    return 1



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
