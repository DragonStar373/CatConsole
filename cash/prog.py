class Program:
    def __init__(self, command, argcount, helpstring):
        self.command = command
        self.argcount = argcount
        self.helpstring = helpstring

    def run(self, arglist):
        if len(arglist) != self.argcount:
            print(self.command + ": Not enough arguments")
            return 1
        #else implied, since it returns



def prog():
    cd = Program("cd", 1, "")
    ls = Program("ls", 0, "")
    mkdir = Program("mkdir", 1, "")
    rmdir = Program("rmdir", 1, "")
    dct = {
        "cd": lambda: print(),
        "ls": lambda: print(),
        "mkdir": lambda: print(),
        "rmdir": lambda: print(),
    }
    return dct