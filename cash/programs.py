from .fs import fs
import sys

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
    "cc": [lambda: exec("break"), 0, ""],
    "help": [lambda: help_func(progs), 0, ""],
    "cd": [lambda arg: fs.dir.cd(arg), 1, ""],
    "ls": [lambda: fs.dir.ls(), 0, ""],
    "mkdir": [lambda arg: fs.dir.mkdir(arg), 1, ""],
    "rmdir": [lambda arg: fs.dir.rmdir(arg), 1, ""],
    "testfunc": [lambda: test_func(), 0, ""],
    "rm": [lambda arg: fs.file.rmfile(arg), 1, ""],
    "del": [lambda arg: fs.file.rmfile(arg), 1, ""],
    "touch": [lambda arg: fs.file.mkfile(arg), 1, ""],
    "retfd": [lambda  arg: fs.file.ret_file_data_from_name(arg), 1, ""],
    "edit": [lambda arg: fs.file.edit_file(arg), 1, ""],
}

