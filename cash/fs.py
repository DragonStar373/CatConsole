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
    lines = []

    def __init__(self, fileName):
        global context
        self.fileName = fileName
        ensure_exists = open(fileName, "a")
        ensure_exists.close()

        self.lines = self._read_file()
        # print(lines)
        if len(self.lines) < 2 or (len(self.lines) > 1 and self.lines[1].strip() != "0"):
            self._init_fs()
            self.lines = self._read_file()
        else:
            self.lines = self._read_file()
        context = int(self.lines[0])


    def _read_file(self):
        with open(self.fileName, "r+") as self.file:
            self.file.seek(0)
            fsLines = self.file.readlines()
            self.file.seek(0)
        return fsLines

    def _write_lines(self,lines):  # for any situation needing to write to file, may need to be expanded on to write only specific lines (seek(line), writeline(), seek(0))
        with open(self.fileName, "w+") as self.file:
            self.file.seek(0)
            self.file.writelines(lines)
            self.file.seek(0)
        self.lines = self._read_file()
        return 0

    def _init_fs(self):  # writes default base root fs format, circa revision 0. writes to file, then moves the file's pointer back to start again
        initarray = ["4\n", "0\n", "1111\n", "0:/::\n"]
        self._write_lines(initarray)
        self.lines = self._read_file()
        print(self.lines, "!!!!!!")
        return

    def ret_ls(self):  # returns an array of all the names of the child objects of context
        lines = self._read_file()
        here = lines[context - 1]  # basically equal to the line of the fs we're currently in
        hereitems = here.split(",")  # array of all the individual components of the current directory

        # adds every child object to an array, then makes an array out of just the names of all the child objects (and returns it)
        ls_list = []
        child_list = []  # note: this name is kinda inaccurate since it actually stores any/every of context's child objects, not just the directories
        n = 0
        for i in hereitems:
            if n != 0:
                child_list.append(lines[int(i) - 1])
                # print(child_list, n, i)
            n = n + 1
        # print(child_list, " <-child_list")
        n = 0
        for i in child_list:
            dirname = i.split(",")[0].split(":")[1]  # for each number in child_list, go to that line, go to first area before a comma, and go to second area between colons (ie where the name of each child object can be found)
            ls_list.append(dirname)
            n = n + 1
        return ls_list

    def ret_objectID(self, name):
        lines = self._read_file()

        if name not in self.ret_ls():
            print("\"" + name + "\" not found")
            return 1

        # looking for what child object matches the provided name
        n = 0
        objectID = 0
        foundID = False  # contingency, realistically there's no reason we shouldn't find the ID if nameexists == True

        for i in lines[context - 1].split(","):
            if n > 0:
                if lines[int(i) - 1].split(":")[1].strip() == name.strip():
                    foundID = True
                    objectID = int(i)
                    break
            n = n + 1

        # just in case; this SHOULD never happen though, right?? :)
        if not foundID:
            print("An unexpected error has occurred. Please go cry in a corner as necessary.")
            return 1

        return objectID

    def ret_object_type(self, objectID):
        lines = self._read_file()
        if self._ensure_exists(objectID):
            return int(lines[objectID - 1].strip().split(":")[0])
        else:
            print("Item does not exist or has no data")
            return False

    def ret_context(self):
        global context
        return context

    def ret_object_type_by_name(self, name):
        objectID = self.ret_objectID(name)
        return self.ret_object_type(objectID)

    def ret_full_path(self, objectID):
        pass #should include object name, with / at the end if it is a dir

    def _mk_child_at_context(self):      #modifies self.lines, returns dirID of child object
        # looking for closest space available to write/overwrite new directory, modifying population array as appropriate
        lines = self.lines
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
        if usingBlankSpace:
            lines[2] = reconstruct + "\n"
        else:
            dirID = n
            reconstruct += "1"
            lines[2] = reconstruct + "\n"
            lines.append("")

        lines[context - 1] = self.lines[context - 1].strip() + "," + str(dirID + 1) + "\n"   #add the child object to current dir
        #lines.append("\n")
        #print("Testing!!! (_mk_child_at_context) lines = " + str(lines))
        self.lines = lines

        return dirID

    def ret_ls_dirIDs(self):
        pass #maybe returns a dict? array? idk

    def _ensure_exists(self, objectID):
        lines = self._read_file()
        # make sure it exists
        if int(objectID) > len(lines):
            return False
        elif lines[objectID - 1] == "\n" or lines[objectID - 1] == "":
            return False
        return True
    
class Dir(FSIO):
    global context
    def __init__(self, fileName):
        super().__init__(fileName)
        self.lines = self._read_file()

    def check_if_dir(self, dirID):
        lines = self._read_file()
        if not self._ensure_exists(dirID):
            return False
        # make sure it's a file
        if lines[dirID - 1].split(",")[0].split(":")[0] == "1":
            return True
        else:
            return False

    def ret_cd(self, name, *startingContext):
        global context
        if len(startingContext) > 0:
            tempContext = startingContext[0]
        else:
            tempContext = context
        lines = self._read_file()
        here = lines[tempContext - 1]  # basically equal to the line of the fs we're currently in
        hereitems = here.split(",")  # array of all the individual components of the current directory

        # see if the command is asking to "cd ..", in which case tempContext is switched to the directory's parent dir (assuming tempContext != root)
        if name == "..":
            if hereitems[0].split(":")[2] != "":
                tempContext = int(hereitems[0].split(":")[2])
                return tempContext
            else:
                return tempContext
        if name == "/":
            return int(self.lines[0])

        # make sure the target directory exists
        herels = self.ret_ls()
        if name not in herels:
            print("No directory named \"" + name + "\"")
            return -1

        # create array of all the child-objects of the current directory; find which one matches the target directory; make sure the target directory is actually a directory, if so then change tempContext to match
        dir_list = []
        n = 0
        targetID = 0
        for i in hereitems:
            if n != 0:
                dir_list.append(lines[int(i) - 1])
                if lines[int(i) - 1].split(",")[0].split(":")[1] == name:
                    targetID = int(i)
                # break
            n = n + 1
        n = 0
        # print(dir_list, targetID)
        for i in dir_list:
            if dir_list[n].split(",")[0].split(":")[1] == name.strip():
                # print("AAAAAA")
                if dir_list[n].split(",")[0].split(":")[0] != "1":
                    print(name + ": Not a directory")
                    return -1
                else:
                    # print("WAWAWAWA")
                    tempContext = targetID
                    return tempContext
            n = n + 1
        print("Something went wrong...")
        return -1

    def arbitrary_cd(self, dirID):
        global context
        self.lines = self._read_file()
        if not self.check_if_dir(dirID):
            print(self.lines[dirID -1].split(",")[0].split(":")[1] + ": Not a directory")
        context = dirID

    def cd(self, name):
        global context
        preserveContext = context
        context = self.ret_cd(name)
        if context == -1 or context == None:
            context = preserveContext
            return 1
        return 0

    def mkdir(self, name):  # assuming the new dir name is valid and available: locates closest free fs line on population array (if any, otherwise just adds to it), uses that line for new dir, and adds line# to current dir and makes dir at that line
        lines = self._read_file()

        # checking that directory can be created
        if ":" in name or "/" in name or "," in name or "\n" in name or " " in name:
            print("Invalid name: cannot contain spaces, \":\", \",\", \"/\", or \"\\n\"")
            return 1
        elif name == "." or name == "..":
            print("Invalid name: directory cannot be named \".\" or \"..\"")
            return 1
        allnames = self.ret_ls()
        for i in allnames:
            if i == name:
                print("An item with that name already exists")
                return 1
        dirID = self._mk_child_at_context()     #after this statement, local "lines" variable no longer necessary as the function automatically alters self.lines
        self.lines[dirID] = "1:" + name + ":" + str(context) + "\n"
        self._write_lines(self.lines)
        return 0

    def rmdir(self, name):
        lines = self._read_file()

        # checking that directory exists and is valid. assuming it is, execution continues in if block
        if ":" in name or "/" in name or "," in name or "\n" in name or " " in name:
            print("Invalid name: cannot contain spaces, \":\", \",\", \"/\", or \"\\n\"")
            return 1
        if name not in self.ret_ls():
            print("No such name: \"" + name + "\"")
            return 1

        # checking context subdir by subdir to find which one matches name
        n = 0
        dirID = 0
        foundID = False  # contingency, realistically there's no reason we shouldn't find the ID if nameexists == True
        for i in lines[context - 1].split(","):
            if n != 0:
                if lines[int(i) - 1].split(",")[0].split(":")[1] == name:
                    dirID = int(i)
                    foundID = True
            n = n + 1

        # just in case; this SHOULD never happen though, right?? :)
        if foundID != True:
            print("An unexpected error has occurred. Please go cry in a corner as necessary.")
            return 1

        # make sure object is a directory, and that it has no child directories of its own

        if lines[dirID - 1].strip().split(",")[0].split(":")[0] == "1":
            n = 0
            for i in lines[dirID - 1].strip().split(","):
                n = n + 1
            if n > 1:
                print("Error: \"" + name + "\" is not empty.")
                return 1
        else:
            print("\"" + name + "\": not a directory")
            return 1

        # delete data at dirID
        lines[dirID - 1] = "\n"

        # remove target directory's entry from context (aaaaaaaaaa)
        rebuildcontext = ""
        working_rebuildcontext = ""
        skip = False
        commacount = 0
        n = 0
        for char in lines[context - 1].strip():  # working_rebuildcontext           #dude. im not even gonna lie. you're gonna have to figure this for block out on your own. it barely works as it is, i don't even wanna waste time documenting it because im 90% sure imma end up needing to change it later anyways
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
                return 1
            if len(lines[context - 1].strip()) == n + 1 and working_rebuildcontext != str(dirID):
                rebuildcontext = rebuildcontext + "," + working_rebuildcontext
                working_rebuildcontext = ""
            n = n + 1

        lines[context - 1] = rebuildcontext + "\n"  # actually do the thing now

        # clear newly freed space from the population array
        n = 0
        rebuild_poparray = ""
        for bit in lines[2].strip():
            if n == (dirID - 1):
                if int(bit) == 1:
                    rebuild_poparray = rebuild_poparray + "0"
                else:
                    print("How unfortunate. An error has occurred. You should probably go check that")  # let's hope this never happens
                    return 1
            else:
                rebuild_poparray = rebuild_poparray + bit
            n = n + 1
        lines[2] = rebuild_poparray + "\n"
        #print(lines)

        # write to file.
        self._write_lines(lines)
        return 0

    def ret_path_at_context(self):
        fslines = self._read_file()
        currentpath = []
        tracecontext = context
        cashpath = ""
        traced = False
        while not traced:
            # print(fslines[tracecontext - 1].split(",")[0].split(":")[0])
            if fslines[tracecontext - 1].split(",")[0].split(":")[0] != "0":
                currentpath.append(fslines[tracecontext - 1].split(",")[0].split(":")[1])
                tracecontext = int(fslines[tracecontext - 1].split(",")[0].split(":")[2])
            if fslines[tracecontext - 1].split(",")[0].split(":")[0] == "0":
                traced = True
                currentpath.append("/")
                break
            currentpath.append("/")
        # print(tracecontext, currentpath)
        if len(currentpath) < 2:
            cashpath = currentpath[0]
        else:
            for i in currentpath[::-1]:  # reverse of array for loop
                cashpath = cashpath + i
        return cashpath

    def ret_path(self, dirID):
        pass #should only be for dirs, / at the end



class File(FSIO):
    global context
    def __init__(self, fileName):
        super().__init__(fileName)
        global context
        self.lines = self._read_file()

    def check_if_file(self, fileID):
        lines = self._read_file()
        if not self._ensure_exists(fileID):
            return False
        #make sure it's a file
        if lines[fileID - 1].split(",")[0].split(":")[0] == "2":
            return True
        else:
            return False

    def _encode_data(self, string):
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

    def _decode_data(self, string):
        reconstruction = ""
        i = 0
        while i < len(string):
            if string[i] == "\\":
                if i + 1 < len(string):
                    next_char = string[i + 1]
                    if next_char == "\\":
                        reconstruction += "\\"
                    elif next_char == "n":
                        reconstruction += "\n"
                    elif next_char == ":":
                        reconstruction += ":"
                    else:
                        reconstruction += "\\" + next_char  # Preserve unknown escape sequences
                    i += 1  # Skip the next character since it was part of an escape sequence
                else:
                    reconstruction += "\\"  # Edge case: trailing backslash
            else:
                reconstruction += string[i]
            i += 1
        return reconstruction

    def _new_file_in_lines(self, name):
        self.lines = self._read_file()
        dirID = self._mk_child_at_context()
        self.lines[dirID] = "2:" + str(name) + ":" + str(context) + "::" + "\n"
        return self.lines

    def mkfile(self, name, *targetContext):
        if ":" in name or "/" in name or "," in name or "\n" in name or " " in name:
            print("Invalid name: cannot contain spaces, \":\", \",\", \"/\", or \"\\n\"")
            return 1
        elif name == "." or name == "..":
            print("Invalid name: file cannot be named \".\" or \"..\"")
            return 1
        allnames = self.ret_ls()
        for i in allnames:
            if i == name:
                print("An item with that name already exists")
                return 1
        self._write_lines(self._new_file_in_lines(name))
        return 0

    def rmfile(self, name):
        lines = self._read_file()

        # checking that directory exists and is valid
        if ":" in name or "/" in name or "," in name or "\n" in name or " " in name:
            print("Invalid name: cannot contain spaces, \":\", \",\", \"/\", or \"\\n\"")
            return 1
        allnames = self.ret_ls()
        nameexists = False
        for i in allnames:
            if i == name:
                nameexists = True
        if not nameexists:
            print("No such name: \"" + name + "\"")
            return

        # looking for what child object matches the provided name
        n = 0
        fileID = 0
        foundID = False  # contingency, realistically there's no reason we shouldn't find the ID if nameexists == True
        for i in lines[context - 1].split(","):
            if n != 0:
                if lines[int(i) - 1].split(",")[0].split(":")[1] == name:
                    fileID = int(i)
                    foundID = True
            n = n + 1

        # just in case; this SHOULD never happen though, right?? :)
        if foundID != True:
            print("An unexpected error has occurred. Please go cry in a corner as necessary.")
            return 1

        # make sure object is a file
        if lines[fileID - 1].strip().split(",")[0].split(":")[0] == "1":
            print("\"" + name + "\": is a directory")
            return 1
        elif lines[fileID - 1].strip().split(",")[0].split(":")[0] != "2":
            print("\"" + name + "\": item of unkown type")
            return 1

        # delete data at fileID
        lines[fileID - 1] = "\n"

        # remove name's entry from context (aaaaaaaaaa)
        rebuildcontext = ""
        working_rebuildcontext = ""
        commacount = 0
        n = 0
        for char in lines[context - 1].strip():  # working_rebuildcontext           #dude. im not even gonna lie. you're gonna have to figure this for block out on your own. it barely works as it is, i don't even wanna waste time documenting it because im 90% sure imma end up needing to change it later anyways
            if working_rebuildcontext == str(fileID) and char == ",":
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
                return 1

            if len(lines[context - 1].strip()) == n + 1 and working_rebuildcontext != str(fileID):
                rebuildcontext = rebuildcontext + "," + working_rebuildcontext
                working_rebuildcontext = ""
            n = n + 1
            #print(rebuildcontext, working_rebuildcontext, skip, char)
        lines[context - 1] = rebuildcontext + "\n"  # actually do the thing now

        # clear newly freed space from the population array
        n = 0
        rebuild_poparray = ""
        for bit in lines[2].strip():
            if n == (fileID - 1):
                if int(bit) == 1:
                    rebuild_poparray = rebuild_poparray + "0"
                else:
                    print(
                        "How unfortunate. An error has occurred. You should probably go check that")  # let's hope this never happens
                    return 1
            else:
                rebuild_poparray = rebuild_poparray + bit
            n = n + 1
        lines[2] = rebuild_poparray + "\n"

        # write to file.
        self._write_lines(lines)

    def write_file_data_from_ID(self, data, fileID):
        lines = self._read_file()

        #checking that fileID is what it says it is
        if not self.check_if_file(fileID):
            print("Error: given object not a file")
            return 1
        if len(lines[fileID - 1].split(":")) < 5:
            print("Error: incorrectly formatted or possibly corrupt file..?")
            return 1

        #encoding the data depending on the provided data's type, appending it to the stub, writing it to lines, and writing lines,
        encodedData = ""
        if isinstance(data, str):
            encodedData = encodedData + self._encode_data(data)
        elif isinstance(data, list):
            for section in data:
                encodedData = encodedData + self._encode_data(section)
        else:
            print("it would interest you to know that you passed an impossible datatype to a function. data being typecast to string;")
            data = str(data)
            encodedData = encodedData + self._encode_data(data)
        #get just the object stub from the line
        fileStub = ""
        n = 0
        for section in lines[fileID - 1].strip().split(":"):
            if n == 4:
                break
            fileStub = fileStub + section + ":"
            n = n + 1
        result = fileStub + encodedData + "\n"
        lines[fileID -1] = result
        self._write_lines(lines)
        return 0

    def write_file_data_from_name(self, data, filename):
        lines = self._read_file()
        global context
        contextLs = self.ret_ls()
        if filename not in contextLs:
            print("No entry named \"" + filename + "\"")
            return 1
        if ":" in filename or "/" in filename or "," in filename or "\n" in filename or " " in filename:
            print("Invalid name: cannot contain spaces, \":\", \",\", \"/\", or \"\\n\"")
            return 1

        # find the id of the target file, make sure target object is in fact a file
        fileID = self.ret_objectID(filename)
        if not self.check_if_file(fileID):
            print("Error: given object not a file")
            return 1
        if len(lines[fileID - 1].split(":")) < 5:
            print("Error: incorrectly formatted or possibly corrupt file..?")
            return 1

        # encoding the data depending on the provided data's type, appending it to the stub, writing it to lines, and writing lines,
        encodedData = ""
        if isinstance(data, str):
            encodedData = encodedData + self._encode_data(data)
        elif isinstance(data, list):
            for section in data:
                encodedData = encodedData + self._encode_data(section)
        else:
            print(
                "it would interest you to know that you passed an impossible datatype to a function. data being typecast to string;")
            data = str(data)
            encodedData = encodedData + self._encode_data(data)
        # get just the object stub from the line
        fileStub = ""
        n = 0
        for section in lines[fileID - 1].strip().split(":"):
            if n == 4:
                break
            fileStub = fileStub + section + ":"
            n = n + 1
        result = fileStub + encodedData + "\n"
        lines[fileID - 1] = result
        self._write_lines(lines)
        return 0

    def edit_file(self, name):
        lines = self._read_file()

        # checking that directory exists and is valid
        if ":" in name or "/" in name or "," in name or "\n" in name or " " in name:
            print("Invalid name: cannot contain spaces, \":\", \",\", \"/\", or \"\\n\"")
            return 1
        if name not in self.ret_ls():
            print("No such name: \"" + name + "\"")
            return 1
        if not self.check_if_file(self.ret_objectID(name)):
            print(name + ": Not a file")
            return 1

        #prompting user for data to write
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
        self.write_file_data_from_name(data, name)
        return 0

    def ret_file_data_from_name(self, filename):
        self.lines = self._read_file()
        global context
        contextLs = self.ret_ls()
        if filename not in contextLs:
            print("No entry named \"" + filename + "\"")
            return 1

        #find the id of the target file, make sure target object is in fact a file
        preHereItems = self.lines[context - 1].split(",")
        hereitems = []      #to contain an array of all the child objects in the current directory
        n = 0
        for i in preHereItems:
            if n > 0:
                hereitems.append(i)
            n = n + 1
        targetLines = ""
        n = 0
        targetID = 0
        for i in hereitems:
            targetLines = targetLines + self.lines[int(i) - 1]
            if self.lines[int(i) - 1].split(",")[0].split(":")[1] == filename:
                targetID = int(i)
            # break
            n = n + 1
        #error handling; should never occur, since if the name is on the _ret_ls list it should in fact be there
        if targetID == 0:
            print("There seems to have been a problem. This is deeply unfortunate.")
            self.lines = self._read_file()
            return 1

        decoded = self.ret_file_data_from_ID(targetID)
        #print(decoded)
        return decoded

    def ret_file_data_from_ID(self, fileID):
        self.lines = self._read_file()
        global context

        if not self.check_if_file(fileID):
            print("Not a file or unknown type")
            return 1

        # fetch the file data, decode it, then return it
        n = 0
        filedata = ""
        filedatalist = []
        for section in self.lines[fileID - 1].strip().split(":"):
            if n + 1 == len(self.lines[fileID - 1].strip().split(":")) and n > 3:
                filedatalist.append(section)
            elif n > 3:  # remember n starts at zero
                filedatalist.append(section + ":")
            n = n + 1
        for section in filedatalist:
            filedata = filedata + section
        decoded = self._decode_data(filedata)
        return decoded

    def ret_path(self, fileID):
        pass #should only be for files



class FS:
    def __init__(self, fileName):
        self.dir = Dir(fileName)
        self.file = File(fileName)



global fs
fs = FS("testing.txt")












