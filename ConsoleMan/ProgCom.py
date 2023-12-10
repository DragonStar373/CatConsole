import sqlite3
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

	while True:
		fox = input(">:")
		for program in c.fetchall():
			if program == fox[0]:
				pass
			elif program == fox[4]:
				pass