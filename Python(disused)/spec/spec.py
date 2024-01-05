#gonna be set up like this. Inside /spec, therell be three folders.
#One will be called "desk", one will be called wastebin, and one will be called floor.
#When files are first created, they'll be put on the desk. That will be the working space.
#Then, they can be "knocked" to either the wastebin or the floor.
#The wastebin will serve as a file purgatory. No longer accesible through spec, but you can still retreive them.
#The floor will be the save area. From there, you can open them back onto the desk, or "sweep" them somewhere else.

#While working on a file, one can issue commands by starting the next line in a ":{command}" format.
#Available commands are ":knock wb" or ":knock floor", both of which will result in closing the file.
#":< delete" will delete the last line you wrote, thus restarting it

#later in the future, the program should be a little cleaner. The program should automatically clear the terminal
#and print out a ui in a manner like:
"""
--------------
spec editor v1
--------------
:from matplotlib import *
:def spec():
:	#we need... to open a file. How do that again?
:	opden = input("Welcome to the Simple Python Editor for CatConsole!\n")
>:
"""
#Where ">:" indicated the current working line.
# Using commands like ":<" or ":>" should let you go back or forwards a line.
#When you're on an occupied line, the line wont start with >:
#Instead, the >: will be moved to the end of the line. Commands like ">:delete" will delete the line
#Otherwise, you can keep writing as if adding to it.
#Jebus thats all I need for now


#for now- need to be able to make a file 
#later, need to be able to read a file line by line

import os
import shutil

class BlankFile:	
	global wroteInBlank
	global hord

	def write(self, content):
		global wroteInBlank
		global hord
		if wroteInBlank == False:
			hord = ""
		hord = hord + content + "\n"
		wroteInBlank = True

	def close(self):
		global wroteInBlank
		if wroteInBlank == True:
			print("You have not chosen a file to write to. Please use :save, or all progress will be lost.")

	def closeopen(self):
		global tryingtocloseopen
		global wroteInBlank
		if wroteInBlank == True:
			#print("You have not chosen a file to write to. Please use :save, or all progress will be lost.")
			tryingtocloseopen = True


def spec():
	global wroteInBlank
	global hord
	global tryingtocloseopen
	wroteInBlank = False
	validknockdestinations = ["wastebin","floor"]
	#we need... to open a file. How do that again?
	
	openc = BlankFile()
	test_list = []
	obj = os.scandir("./spec/desk")
	for entry in obj:
		if entry.is_file():
			test_list.append(entry.name)

	print("Welcome to the Simple Python Editor for CatConsole!")
	if test_list:
		for entry in test_list:
			if entry == ".DS_Store":
				os.remove("./spec/desk/.DS_Store")
				pass
		try:
			discardable = test_list[1]
			if test_list:
				
				print("File(s) open:")
				for entry in test_list:
					print(entry)
				print("\nUse :open to add to these, or use :help for more information")
		except IndexError:
			pass



	while True:
		fox = input(":")#fox is only used to receive input. it is not used later, as it is replaced by command & commandkey
		try:
			if fox[0] == ":":
				command = fox.split(":")[1]#command is anything after the :
				commandkey = fox.split(":")[1].split()[0]#commandkey is the first full word after :
			else:
				command = None
				commandkey = None
					
		except IndexError:
			command = None
			commandkey = None

		if command != None:#if there is for certain a command being excecuted, it goes through the list of commands

			if command == "help":
				input("Welcome to spec, the simple python editor for CatConsole!")
				input("In spec, you can create and edit files using comands.")
				input("To use these commands, type \":\" followed by whatever command you want to enter.")
				input("For instance, to create a new file, type \":open example.txt\"")
				input("This will create a new file named example.txt on the desk.")
				input("Once you have a file opened, just start typing!")
				input("spec writes to files line by line, so every time you press enter, your progress is saved.")
				input("At any point while writing to your file, you can issue a command by starting the line with \":\"")
				input("When you're done, use \":knock\" to move it off your desk.")
				input("spec has two other locations besides the desk: the floor, and the wastebin.")
				input("The floor is the final 'save' location for your files. From there, you can move them where you want.")
				input("If you want to discard your file, you can instead knock it to the wastebin. It's not gone for good, but close.")
				input("When you finish writing to a file, use \":knock floor\" to save it, or \":knock wb\" to delete it.")
				input("You can always open a file from the floor with \":open (file)\" -but remember, you can only add to it.")
				input("That's spec! Current functionality is limited for now, but more is planned for the future.")
			elif commandkey == "help":#this works bc were using elif, so if the whole command is "help", itll just excecute the above. if not, itll get to here.
				print("at some point, make a specific help for each command")
			elif commandkey == "read":
				try:
					if command.split()[1] == "-floor":
						with open("./spec/floor/" + command.split()[2]) as my_file:
							for line in my_file:
								input(line)
					elif command.split()[1] == "-wastebin":
						with open("./spec/wastebin/" + command.split()[2]) as my_file:
							for line in my_file:
								input(line)
					elif command.split()[1] == "-desk" or command.split()[1]:
						with open("./spec/wastebin/" + command.split()[2]) as my_file:
							for line in my_file:
								input(line)
					elif command.split()[1][0] == "-":
						if command.split()[1].split("-")[1][0] == ".": 
							with open(command.split()[1].split("-")[1] +  "/" + command.split()[2]) as my_file:
								for line in my_file:
									input(line)
				except IndexError:
					print(":read usage: :read -<destination> <file>")
					print("examples:\n:read -floor file.txt\n:read -./ConsoleMan ProgCom.py")

			elif commandkey == "quit" or commandkey == "exit":
				break
			
			try:
				if commandkey == "open":#at this point, i should say that any files being created on the desk will be a, while floor will be a
					if wroteInBlank == True:
						try:
							openc.closeopen()
						except AttributeError:
							print("AttributeError 00 - Unknown cause. Stability may vary. Please :save and :quit, and reopen spec.")
					if True:
						currentFile = command.split()[1]
						openc = open("./spec/desk/" + currentFile, "a")
						print("Opening " + currentFile)
						wroteInBlank = False
					else:#I think I no longer need this code below
						openOverBlank = input("Do you still want to proceed?:")
						if openOverBlank.lower() == "yes" or openOverBlank.lower() == "y":
							currentFile = command.split()[1]
							openc = open("./spec/desk/" + currentFile, "a")
						print("Opening " + currentFile)
						wroteInBlank = False

			except IndexError:
				print("Please enter a parameter")

			try:
				if commandkey == "knock":
					if command.split()[1] == "floor" or command.split()[1] == "f":
						openc.close()
						openc = BlankFile()
						shutil.copy("./spec/desk/" + currentFile, "./spec/floor/" + currentFile)
						os.remove("./spec/desk/" + currentFile)
					elif command.split()[1] == "wastebin" or command.split()[1] == "wb":
						openc.close()
						openc = BlankFile()
						shutil.copy("./spec/desk/" + currentFile, "./spec/wastebin/" + currentFile)
						os.remove("./spec/desk/" + currentFile)
					else:
						print("Invalid knock destination. Valid destinations:")
						print(validknockdestinations)
						
			except IndexError:
				print("Please enter a parameter")

			if commandkey == "close":
				try:
					openc.close()
					openc = BlankFile()
				except ValueError:
					openc = BlankFile()

			if commandkey == "save":
				if wroteInBlank == True:
					try:
						currentFile = command.split()[1]
						openc = open("./spec/desk/" + currentFile, "a")
						openc.write(hord)
						print("Now editing " + command.split()[1])
						wroteInBlank = False
					except IndexError:
						saveBlank = input("Save file as:")
						currentFile = saveBlank
						openc = open("./spec/desk/" + saveBlank, "a")
						openc.write(hord)
						print("Now editing " + saveBlank)
						wroteInBlank = False



				else:
					openc.close()
					openc = open("./spec/desk/" + currentFile, "a")

				


		else:
			openc.write(fox + "hoy")

			if wroteInBlank == True:
				pass


			

















