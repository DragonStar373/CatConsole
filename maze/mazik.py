from maze_tools import make_maze, cell_find, animate_maze_and_path

size = int(input("give size"))
N = "N"
S = "S"
W = "W"
E = "E"
facing = "N"
global finished
finished = False
#global r
#global c
#global oddwin
r = 0
c = 0
path = []

oddwin = make_maze(size,size)
#print(oddwin)
currentcell = cell_find(oddwin, r, c)
#print_maze(oddwin, 2, 2)
#print(currentcell["N"])




def mazik():
    
    #HAPPY BIRTHDAY ODDWIN
    
    global N
    global S
    global W
    global E
    global facing
    global finished
    global r
    global c
    global oddwin
    global path
    global currentcell
    print(currentcell)
    path.append(currentcell)
    
    #checks if it can go right, if it can then it changes direction immidatly
    
            


    
    
    
    
    
    #checks if it can go forward, if it does it makes the move(goforwarsd()) and if it cant then it rotates left(turnleft())
 
    
    
    
    #WHEEEEWWWWWWWWWWWW
    #currentcell{facing}
    #while finished == False:#rotates right if the space is open; goes forward if it can, rotates left if it cant
    for i in range(999999999):
        
        if finished == False:
            checkright(facing)#turns right if can
            checkforward(facing)
            turnleft(facing)
            print(currentcell)
            print("\ncurrent cell ^")
            print(facing)
            print("")
            print("\nTHIS IS I = " + str(i) + "\n")
            if currentcell['row'] == (size-1) and currentcell['col'] == (size - 1):
                print("HECK YEAH WE DID IT WOOOOOOOOOOOOOOO")
                finished = True
                animate_maze_and_path(oddwin, path, size, size)
                break
        # if the current cells row = size-1 and col = size - 1
    
    
    
    
def checkforward(facing):#still need a go forward and turn left
    print("\nrunning checkforward")
    if facing == "E":
        if currentcell["E"] == True:
            print("we checked e to go f")
            goforward(facing)
            return
        else:
            turnleft(facing)
            return
    elif facing == "N":
        if currentcell["N"] == True:
            print("we checked n to go f")
            goforward(facing)
            return
        else:
            print("n turning l to w")
            turnleft(facing)
            return
    elif facing == "W":
        if currentcell["W"] == True:
            print("we checked w to go f")
            goforward(facing)
            return
        else:
            turnleft(facing)
            print("w turning left to s")
            return
    elif facing == "S":
        if currentcell["S"] == True:
            print("we checked s to go f")
            goforward(facing)
            return
        else:
            turnleft(facing)
            return

def turnleft(funfacing):#rotates left
    print("running turnleft")
    global facing
    if funfacing == "N":
        if currentcell["E"] == False:
            facing = "W"
            print("turned left to w\n")
        elif funfacing == "W":
            if currentcell["N"] == False:
                facing = "S"
                print("turned left to s\n")
        elif funfacing == "S":
            if currentcell["W"] == False:
                facing = "E"
                print("turned left to e\n")
        elif funfacing == "E":
            if currentcell["S"] == False:
                facing = "N"
                print("turned left to n\n")
                
def goforward(funfacing):#changes uggh out of time sry futrue me
    print("\nrunning gofoward")
    global currentcell
    global r
    global c
    if funfacing == "N":
        r = r + 1
        currentcell = cell_find(oddwin, r, c)
        print("went north")
    elif funfacing == "E":
        c = c + 1
        currentcell = cell_find(oddwin, r, c)
        print("went e")
    elif funfacing == "S":
        r = r - 1
        currentcell = cell_find(oddwin, r, c)
        print("went s")
    elif funfacing == "W":
        c = c - 1
        currentcell = cell_find(oddwin, r, c)
        print("went w")
    path.append(currentcell)
    
    
def checkright(funfacing):
    global facing
    global currentcell
    if funfacing == "N":
        #print("got to this if statement")
        if currentcell["E"] == True:
            print("echecked n to turn right to e\n")
            facing = "E"
            
            
        elif funfacing == "W":
                if currentcell["N"] == True:
                    facing = "N"
        
        elif funfacing == "S":
            if currentcell["W"]:
                facing = "W"
        
        elif funfacing == "E":
            if currentcell["S"]:
                facing = "S"
                print("in checkright facing = " + facing)