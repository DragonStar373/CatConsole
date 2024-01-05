import sqlite3
import importlib
'''
so pc is going to manage everything catconsole already does- it will access the db of current programs, and every time
a command is entered it will search the db for the specific program and when it finds a match, it will excecute the required
function in the required destination/file. The db schema will have the primary command to access the function, the primary
funtion to run, the destination from CatConsole where the function is located, and any other commands that can be used to
excecute the same function (ie secondary commands)

'''

def prog_com():
	print("progcom1")
	conn = sqlite3.connect(r"./ConsoleMan/man.db")
	c = conn.cursor()
	c.execute("SELECT * FROM progcom")
	fork = []
	while True:
		fox = input(">:")
		for program in c.fetchall():
			print(program)
			if program[0] == fox:#The following code, step by step- looks for a match between input and an actual program
				print(program[0])
				for letter in program[1]:#goes letter by letter, and turns the db path of the file into a list of each letter
					fork.append(letter)

				fork.pop(0)#takes off first letter- first letter of db path is always /, which isnt useful to us
				tempfork = fork#creates version of fork we can base on while changes are made to fork

				for letter in tempfork:#goes through fork and identifies any / and replaces with .
					if letter == "/":
						fork[fork.index(letter)] = "."


				finpath = fork[0]
				fork.pop(0)
				for letter in fork:
					finpath = finpath + letter
				print(finpath)
				finpath.pop()
				
				importlib.import_module(finpath)
			elif program[4] == fox:
				pass



