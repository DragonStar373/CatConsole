import time
import sys

from carmode import carmode
from REPEATINGCAT import rcat
#from maze.mazik import mazik

global file
global context

def initFS():
    initarray = ["4\n","0\n","1111\n","0:/::\n"]
    file.writelines(initarray)
    file.seek(0)
    return

def cd(name):
    global context
    lines = file.readlines()
    file.seek(0)
    ls_list = []
    dir_list = []
    here = lines[context - 1]
    hereitems = here.split(",")
    #print(hereitems, " <-hereitems")

    #see if its .. and act accordingly
    if name == "..":
        if hereitems[0].split(":")[2] != "":
            context = int(hereitems[0].split(":")[2])
            return
        else:
            return

    #make sure it exists
    herels = ret_ls()
    if name not in herels:
        print("No directory named \"" + name + "\"")
        return
    #make sure it's a directory

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


def ret_ls():
    ls_list = []
    dir_list = []
    lines = file.readlines()
    #print(lines)
    file.seek(0)
    here = lines[context-1]
    #print(here)
    hereitems = here.split(",")
    #print(hereitems, " <-hereitems")
    n = 0
    for i in hereitems:
        if n != 0:
            dir_list.append(lines[int(i) - 1])
            #print(dir_list, n, i)
        n = n + 1
    #print(dir_list, " <-dir_list")
    n = 0
    for i in dir_list:
        dirname = dir_list[n].split(",")[0].split(":")[1] #for each number in dir_list, go to that line, go to first area before a comma, and go to second area between colons
        ls_list.append(dirname)
        n = n + 1
    return ls_list

def ls():
    local_ret_ls = ret_ls()
    localls = ""
    for i in local_ret_ls:
        localls = localls + i + " "
    print(localls)
    return

def mkdir(name):
    lines = file.readlines()
    file.seek(0)
    #print(lines)
    # checking that directory can be created
    if ":" in name or "/" in name or "," in name or "\n" in name or " " in name:
        print("Invalid name: cannot contain spaces, \":\", \",\", \"/\", or \"\\n\"")
        return
    allnames = ret_ls()
    for i in allnames:
        if i == name:
            print("That name already exists")
            return
    # looking for closest space available to write/overwrite new directory, modifying population array as appropriate
    n = 0
    dirID = n   # dirID will be in array form (ie if the file line is 5, the notation would be [4]; basically [X + 1])
    reconstruct = ""
    usingBlankSpace = False
    #print(len(lines[2].strip())) #<--this is the length of the POPULATION ARRAY!!! NOT lines!!!
    for item in lines[2].strip():
        if int(item) == 0 and usingBlankSpace == False:
            usingBlankSpace = True      #goes thru list of ones & zeroes, converts the first zero it gets to into a 1
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
    #print(lines, dirID)
    #modifying the context as appropriate
    lines[context - 1] = lines[context - 1].strip() + "," + str(dirID + 1) + "\n"
    #actually creating the content
    lines[dirID] = "1:" + name + ":" + str(context) + "\n"
    #print(lines)
    file.writelines(lines)
    file.seek(0)
    return

def rmdir(name):
    lines = file.readlines()
    file.seek(0)
    # checking that directory exists
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
        #delete data at dirID
        lines[dirID - 1] = "\n"
        #remove name's entry from context
        rebuildcontext = ""
        working_rebuildcontext = ""
        skip = False
        commacount = 0
        n = 0
        for char in lines[context - 1].strip():
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

            if len(lines[context - 1].strip()) == n + 1 and working_rebuildcontext != str(dirID):
                rebuildcontext = rebuildcontext + "," + working_rebuildcontext + "\n"
                working_rebuildcontext = ""
            n = n + 1
            #print(rebuildcontext, working_rebuildcontext, skip, char)
        #print(lines, rebuildcontext)
        #clear newly freed space from the population array
        #!!!!!! WORK FROM HERE, JUST FINISH POP. ARRAY !!!!!!
    else:
        print("No such name: \"" + name + "\"")
        return
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
                    else:
                        print("\"" + cashcat.split(" ")[1] + "\" is not a recognized command, or more likely has not been integrated")




            elif cashcat == "car":
                carmode()
            elif cashcat == "cash":
                cash()
            elif cashcat == "nyan":
                from nyan import nyanfunction
                nyanfunction()
            elif cashcat == "maze":
                from mazik.mazik import mazik
                print("make sure you run catconsole with 'python catconsole.py'")
                mazik()
            elif cashcat.lower() == "rcat" or cashcat.lower() == "repeatingcat":
                rcat()
            elif cashcat == "":
                pass
            elif cashcat.lower() == "motd":
                with open("consoleopener.txt", "r+") as f:
                    f.write(input("  >:"))
            else:
                print('"' + cashcat + '" is not a recognised command')



#while True:
#    fox = input(">:")
#    if fox == "quit":
#        break
#    elif fox == "help":
#        print("Public Commands:\n  help\n  maze\n  nyan\n  rcat\n  car\n  quit")
#    elif fox == "car":
#        carmode()
#    elif fox == "nyan":
#        from nyan import nyanfunction
#
#        nyanfunction()
#    elif fox == "maze":
#        from mazik.mazik import mazik
#        print("make sure you run catconsole with 'python catconsole.py'")
#        mazik()
#    elif fox.lower() == "rcat" or fox.lower() == "repeatingcat":
#        rcat()
#    elif fox == "":
#        pass
#    elif fox.lower() == "motd":
#        with open("consoleopener.txt", "r+") as f:
#            f.write(input("  >:"))
#    else:
#        print('"' + fox + '" is not a recognised command')
#
#print("Goodbye")













