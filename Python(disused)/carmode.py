import time
import sys
import os
import random
def startcon():
    global started
    global at
    global hour
    global nextday
    global day
    global naturaltimepass
    global married
    global dstatsettings
    global dstatstartup
    global dstatprompt
    global displaystats
    global homefood
    global timehour
    global tempds
    global crazyval
    global money
    global foodchoice
    global havefood
    global homefood
    global hunger
    global foodisfries
    global dealop
    global car
    global carver
    global restart
    restart = True
    car = False
    started = False
    at = "Home"
    married = False
    day = "Monday"
    havefood = False
    hunger = 100
    naturaltimepass = True
    hour = 6
    timehour = ""
    nextday = False
    dstatsettings = False
    dstatstartup = True
    dstatprompt = False
    displaystats = ""
    homefood = 0
    foodisfries = False
    tempds = 0
    money = 0
    crazyval = 0
    foodchoice = 0
    #needed: huinger
    dealop = False
    carver = "bad"
    
startcon()
def carmode():
    global started
    global at
    global hour
    global nextday
    global day
    global naturaltimepass
    global married
    global dstatsettings
    global dstatstartup
    global dstatprompt
    global displaystats
    global homefood
    global timehour
    global tempds
    global crazyval
    global money
    global foodchoice
    global havefood
    global homefood
    global hunger
    global foodisfries
    global dealop
    global carver
    global restart
    global car
    if restart == True:
        restart = False
        if hour >=12:
            if hour == 24:
                timehour = "12 AM"
            elif hour == 12:
                timehour = "12 PM"
            else:
                timehour = (str(hour - 12)+" PM")
        else:
            timehour = (str(hour) + " AM")
        print("CARMODE!")
        car = True
        time.sleep(1)
        if dstatstartup == True:
            statblock()
            time.sleep(4)
    else:
        car = True
        
    #-----------------------------------
    while car:#loop start
        if hour >=12:
            if hour == 24:
                timehour = "12 AM"
            elif hour == 12:
                timehour = "12 PM"
            else:
                timehour = (str(hour - 12)+" PM")
        else:
            timehour = (str(hour) + " AM")
        if dstatsettings == True and dstatstartup == False and dstatprompt == False:
            displaystats = "On Settings"
        elif dstatsettings == True and dstatstartup == True and dstatprompt == False:
            displaystats = "On Settings and Startup"
        elif dstatsettings == True and dstatstartup == True and dstatprompt == True:
            displaystats = "On Settings Startup and Prompt"
        elif dstatsettings == False and dstatstartup == True and dstatprompt == True:
            displaystats = "On Startup and Prompt"
        elif dstatsettings == False and dstatstartup == False and dstatprompt == True:
            displaystats = "On Prompt"
        elif dstatsettings == False and dstatstartup == True and dstatprompt == False:
            displaystats = "On Startup"
        else:
            displaystats = "Command Only"
        
        if nextday == True:
            if day == "Monday":
                day = "Tuesday"
            elif day == "Tuesday":
                day = "Wednesday"
            elif day == "Wednesday":
                day == "Thursday"
            elif day == "Thursday":
                day = "Friday"
            elif day == "Friday":
                day = "Saturday"
            elif day == "Saturday":
                day = "Sunday"
            elif day == "Sunday":
                day = "Monday"
        if naturaltimepass == True:
            hour = hour + 1
            if hour >= 24:
                hour = 0
                nextday = True
        crazyval = random.randint(1,2)
        hunger = hunger - crazyval
        if hunger < 5:
            print("You're almost out of energy!")
        elif hunger < 15:
            print("You need to eat!")
        if hunger <= 0:
            death()
        
        if dealop == True:
            dealop = False
        if random.randint(1,10) == 2:
            if dealop == False:
                dealop = True
                print("an opportunity has arisen...")
        
        
        
        #Begin prompt
        
        if dstatprompt == True:
            statblock()
        carprompt = input("car:")
        if carprompt.lower() == "start":
            if started == False:
                started = True
                print("car started!")
            else:
                print("car already started.")
        elif carprompt.lower() == "quit" or carprompt.lower() == "exit":
            car = False
            restart = False
        elif carprompt.lower() == "restart":
            car = False
            restart = True
            startcon()
            opener = "consoleopener.txt"
            with open(opener) as nameillneveruseagain:
                startmsg = nameillneveruseagain.read()


            print(startmsg)
        elif carprompt.lower() == "stop":
            if started == True:
                started = False
                print("car stopped.")
            else:
                print("car already stopped.")
        elif carprompt.lower() == "quitall":
            quit()
        elif carprompt.lower() == "":
            pass
        #Drive
        
        elif carprompt == "drive":
            if started == True:
                while True:
                    print("where would you like to go?")
                    destination = input(" >:")
                    if destination.lower() == "help":
                        print("Destinations:\n  Home\n  Work\n  Church\n  McDonalds\n  Dealership")
                    #Home
                    elif destination.lower() == "home":
                        if at == "Home":
                            print("already here bud")
                        else:
                            print("going home!")
                            time.sleep(1)
                            print("")
                            time.sleep(1)
                            print("")
                            time.sleep(1)
                            print("Welcome home")
                            time.sleep(.3)
                            if married == True:
                                print("honey im homeee")
                                time.sleep(.3)
                            at = "Home"
                            break
                    #Work
                    elif destination.lower() == "work":
                        if at == "Work":
                            print("you're already at work")
                        else:
                            print("going to work")
                            if married == True and at == "Home":
                                time.sleep(1)
                                print("bye honey!")
                            time.sleep(1)
                            print("")
                            time.sleep(1)
                            print("")
                            time.sleep(1)
                            print("Welcome to work!")
                            if day == "Sunday" or day == "Saturday":
                                print("...why are you here on a weekend???")
                            if day == "Monday":
                                time.sleep(.4)
                                print("(uggh mondays)")
                                time.sleep(.6)
                            at = "Work"
                            break
                    #Church
                    elif destination.lower() == "church":
                        if at == "Church":
                            print("you're already here... and someone is waiting for you")
                        else:
                            print("going to church")
                            time.sleep(1)
                            print("")
                            time.sleep(1)
                            print("")
                            time.sleep(1)
                            print("Welcome to church!")
                            at = "Church"
                            break
                    #McDonalds
                    elif destination.lower() == "mcdonalds":
                        if at == "McDonalds":
                            print("bro you're already here")
                        else:
                            print("going to mcdonalds")
                            time.sleep(1)
                            print("")
                            time.sleep(1)
                            print("")
                            time.sleep(1)
                            print("Welcome to McDonald!")
                            at = "McDonalds"
                            break
                    #Quit
                    elif destination.lower() == "quit":
                        break
                        #add more destincations here
                    elif destination.lower() == "dealership":
                        if at == "Dealership":
                            print("good job you're here")
                        else:
                            if dealop == True:
                                print("Going to the dealership...")
                                time.sleep(.5)
                                print("")
                                time.sleep(.5)
                                print("")
                                time.sleep(.5)
                                time.sleep(.5)
                                print("")
                                time.sleep(.5)
                                print("")
                                time.sleep(.5)
                                time.sleep(.5)
                                print("")
                                time.sleep(.5)
                                print("")
                                time.sleep(.5)
                                print("WELCOME")
                                at = "Dealership"
                                break
                            else:
                                break
                    elif carver == "good":
                        #extra places
                        if destination.lower() == "":
                            break
                    #end extra places
                    else:
                        print("invalid destination")
            else:
                print("car not started!") 
        
        #Help
        
        elif carprompt == "help":
            print("Available actions:\n  settings\n  quit\n  stats")
            if started == True:
                print("  stop\n  drive")
            else:
                print("  start")
            if at == "Home":
                if havefood == True:
                    print("  put food in fridge")
            if havefood == True:
                print("  eat")
            if at == "Work":
                print("  work")
            if at == "Church":
                if married == False:
                    print("  get married")
            if at == "McDonalds":
                print("  get food")
            if at == "Dealership":
                print("  buy new car")
        
        #Settings
        
        elif carprompt == "settings":
            while True:
                print("\nCARMODE SETTINGS\n________________")
                setprom = input("  >:")
                #Help
                if setprom.lower() == "help":
                    print("  Available Settings:")
                    print("  Day = " + day)
                    print("  Natural_Time_Pass = " + str(naturaltimepass))
                    print("  Display stats = " + str(displaystats))
                #ntp
                elif setprom.lower() == "natural_time_pass" or setprom.lower() == "natural time pass" or setprom.lower() == "ntp":
                    if naturaltimepass == True:
                        naturaltimepass = False
                        print("ntp off")
                    elif naturaltimepass == False:
                        naturaltimepass = True
                        print("ntp on")
                #quit
                elif setprom.lower() == "quit" or setprom.lower() == "exit":
                    break
                    dayprompt = input("Day: ")
                    if dayprompt.lower() == "monday":
                        day = "Monday"
                    elif dayprompt.lower() == "tuesday":
                        day = "Tuesday"
                    elif dayprompt.lower() == "wednesday":
                        day == "Wednesday"
                    elif dayprompt.lower() == "thursday":
                        day = "Thursday"
                    elif dayprompt.lower() == "friday":
                        day = "Friday"
                    elif dayprompt.lower() == "saturday":
                        day = "Saturday"
                    elif dayprompt.lower() == "sunday":
                        day = "Sunday"
                    else:
                        print("please enter valid day")
                #Stats
                elif setprom.lower() == "displaystats" or setprom.lower() == "display stats" or setprom.lower() == "display_stats" or setprom.lower() == "ds" or setprom.lower() == "dis stats":
                    print("Display Stats on:\n 1: Settings menu\n 2: Startup\n 3: Prompt(not reccomended)\n")
                    try:
                        tempds = int(input("  >:"))
                        if tempds == 1:
                            if dstatsettings == False:
                                dstatsettings = True
                                print("Display On Settings ON")
                                print("  (Display settings will take affect after closing settings menu)" + "\033")
                            elif dstatsettings == True:
                                dstatsettings = False
                                print("Display On Settings OFF")
                                print("  (Display settings will take affect after closing settings menu)" + "\033")
                        if tempds == 2:
                            if dstatstartup == False:
                                dstatstartup = True
                                print("Display On Startup ON")
                                print("  (Display settings will take affect after closing settings menu)" + "\033")
                            elif dstatstartup == True:
                                dstatstartup = False
                                print("Display On Startup OFF")
                                print("  (Display settings will take affect after closing settings menu)" + "\033")
                        if tempds == 3:
                            if dstatprompt == False:
                                dstatprompt = True
                                print("Display On Prompt ON")
                                print("  (Display settings will take affect after closing settings menu)" + "\033")
                            elif dstatprompt == True:
                                dstatprompt = False
                                print(" Display On Prompt OFF")
                                print("  (Display settings will take affect after closing settings menu)" + "\033")
                        if tempds != 1 and tempds != 2 and tempds != 3:
                            print("please enter a valid number")
                    except ValueError:
                        print("please enter a valid number")
                else:
                    print("Setting: " + setprom + " not found")
         
        #Help   
         
        elif carprompt.lower() == "stats":
            statblock()
        elif carprompt == "get married":
            if at == "Church" and married == False:
                print("We are gathered here today in the sight of God and these witnesses to join together [Name] and [Name] in holy matrimony;\n which is an honorable estate, instituted of God, since the first man and the first woman walked on the earth.\n Therefore; it is not to be entered into unadvisedly or lightly, but reverently and soberly.\n Into this holy estate, these two persons present come now to be joined.\n Therefore, if anyone can show just cause why they may not be lawfully joined together, let them speak now or forever hold their peace")
                time.sleep(10)
                print("A reading from the Apostle Paul, The first letter to the Corinthians, Chapter 13, verses 4 through 7:\n Love is patient, love is kind. It does not envy, it does not boast, it is not proud.\n It is not rude, it is not self-seeking, it is not easily angered, it keeps no record of wrongs.\n Love does not delight in evil but rejoices with the truth. It always protects, always trusts, always hopes, always perseveres.\n Father, as [Name] and [Name] pledge themselves to each other, help them and bless them that their love may be pure, and their vows may be true.\n Through Jesus Christ our Lord, Amen")
                time.sleep(10)
                married = True
                
        #work
                
        elif carprompt.lower() == "work":
            if at == "Work":
                load_animation()#totes didnt steal this
                print("Worked!")
                crazyval = random.randint(0,9)
                money = money + crazyval
                hour = hour + 4
                
        #get food
                
        elif carprompt.lower() == "get food":
            if at == "McDonalds":
                if havefood == False:
                    crazyval = random.randint(1,4)#for specials later
                    print('"Welcome to McDonalds, whats your order?"')
                    print("1:Burger 6$")
                    print("2:Chicken sandwhich 6$")
                    print("3:McNugget 6$")
                    print("4:Fries 5$(fast, less food)")
                    try:
                        foodchoice = int(input("  >:"))
                        if foodchoice == 1:
                            if money > 5:
                                print('"Alright, Ill have that right out."')
                                time.sleep(3)
                                print('"ONE BURGER!"')
                                time.sleep(3)
                                print('"WHAT?"')
                                time.sleep(3)
                                print('"NO, I SAID B U R G E R!"')
                                time.sleep(.75)
                                print("")
                                time.sleep(.75)
                                print("")
                                time.sleep(.75)
                                print('"Here you go, have a nice day."')
                                print("got food")
                                havefood = True
                                foodisfries = False
                                money = money - 6
                            else:
                                print("sorry, you dont have enough money")
                        elif foodchoice == 2:
                            if money > 5:
                                
                                print('"Alright, Ill have that right out."')
                                time.sleep(3)
                                print('"TERRY!!"')
                                time.sleep(3)
                                print('"DO WE HAVE ANY MORE CHICKEN SANDWHICHES?"')
                                time.sleep(3)
                                print('"...crap..."')
                                time.sleep(.75)
                                print("")
                                time.sleep(.75)
                                print("")
                                time.sleep(.75)
                                print('"Uhh, heres your chicken sandwhich sir"')
                                time.sleep(1)
                                print("(it's not a chicken sandwhich)")
                                time.sleep(.75)
                                print("you got food")
                                havefood = True
                                foodisfries = False
                                money = money - 6
                            else:
                                print("sorry, you dont have enough money")
                        elif foodchoice == 3:
                            if money > 5:
                                print('"Alright, Ill have that right out."')
                                time.sleep(3)
                                print('"JULIA, WE GOT A NUGGET COMING."')
                                time.sleep(3)
                                print('"I. DONT. CARE. IF YOURE ABOUT TO GO ON BREAK."')
                                time.sleep(3)
                                print('"HEY- NO- WHERE ARE YOU GOING?? UGHHH GUESS I HAVE TO DO IT MYSELF."')
                                time.sleep(.75)
                                print("")
                                time.sleep(.75)
                                print("")
                                time.sleep(.75)
                                print('"Here you go, have a nice day."')
                                print("got food")
                                havefood = True
                                foodisfries = False
                                money = money - 6
                            else:
                                print("sorry, you dont have enough money")
                        elif foodchoice == 4:
                            if money > 4:
                                
                                print('"Heres your fries."')
                                print("got food")
                                print("(eating it here bc it'd be hard to make it do otherwise)")
                                regainfood(10, True, 7)
                                #havefood = True
                                #foodisfries = False
                                money = money - 5
                            else:
                                print("too broke for fries lol")
                        else:
                            print("Invalid entry")
                    except ValueError:
                        print("Invalid entry")
                else:
                    print("you can only have one food at a time, take it home to store it")
        elif carprompt.lower() == "eat":
            if at == "Home":
                if homefood > 0:
                    print("eating from fridge")
                    homefood = homefood - 1
                    regainfood(20, True, 3)
                else:
                    if havefood == True:
                        print("eating...")
                        havefood = False
                        regainfood(25, False, 1)
                    else:
                        print("You have no food to eat")
            else:
                if havefood == True:
                    print("eating...")
                    havefood = False
                    regainfood(25, False, 1)
                else:
                    print("You have no food to eat")
        elif carprompt.lower() == "put food in fridge":
            if at == "Home":
                if havefood == True:
                    havefood = False
                    homefood = homefood + 1
                    print("done")
                else:
                    print("you have no food")
            else:
                print("you're not at home")
        
        elif carprompt.lower() == "buy new car":
            if at == "Dealership":
                salva = str(input("Do you want to reset all progress and get a new, better car?"))
                if salva.lower() == "y" or salva.lower() == "yes" or salva.lower() == "yeah" or salva.lower() == "yerp" or salva.lower() == "yup" or salva.lower() == "sure":
                    startcon()
                    carver = "good"
                    time.sleep(.2)
                    print("")
                    time.sleep(.2)
                    print("")
                    time.sleep(.2)
                    print("")
                    time.sleep(.2)
                    print("")
                    time.sleep(.2)
                    print("")
                    time.sleep(.2)
                    print("")
                    time.sleep(.2)
                    print("")
                    time.sleep(.2)
                    print("")
                    time.sleep(.2)
                    print("")
                    time.sleep(.2)
                    print("")
                    time.sleep(.2)
                    print("")
                    time.sleep(.2)
                    print("")
                    time.sleep(.2)
                    print("")
                    time.sleep(.2)
                    print("")
                    car = False
                    opener = "consoleopener.txt"
                    with open(opener) as nameillneveruseagain:
                        startmsg = nameillneveruseagain.read()


                    print(startmsg)
                else:
                    print("are you sure? this is a rare opportunity!")
                    salva = str(input("Do you want to reset all progress and get a new, better car?"))
                    if salva.lower() == "y" or salva.lower() == "yes" or salva.lower() == "yeah" or salva.lower() == "yerp" or salva.lower() == "yup" or salva.lower() == "sure":
                        startcon()
                        carver = "good"
                        time.sleep(.2)
                        print("")
                        time.sleep(.2)
                        print("")
                        time.sleep(.2)
                        print("")
                        time.sleep(.2)
                        print("")
                        time.sleep(.2)
                        print("")
                        time.sleep(.2)
                        print("")
                        time.sleep(.2)
                        print("")
                        time.sleep(.2)
                        print("")
                        time.sleep(.2)
                        print("")
                        time.sleep(.2)
                        print("")
                        time.sleep(.2)
                        print("")
                        time.sleep(.2)
                        print("")
                        time.sleep(.2)
                        print("")
                        time.sleep(.2)
                        print("")
                        car = False
                        opener = "consoleopener.txt"
                        with open(opener) as nameillneveruseagain:
                            startmsg = nameillneveruseagain.read()


                        print(startmsg)
                    else:
                        break
                        
        else:
            print("'" + carprompt + "' is not a valid command")
            

def regainfood(reg, isrand, spec):
    global hunger
    rand1 = reg - spec
    rand2 = reg + spec
    if isrand == False:
        hunger = hunger + reg
        if hunger > 100:
            hunger = 100
    else:
        crey = random.randint(rand1, rand2)
        hunger = hunger + crey
        if hunger > 100:
            hunger = 100
def load_animation():
  
    # String to be displayed when the application is loading
    load_str = "Working..."
    ls_len = len(load_str)
  
  
    # String for creating the rotating line
    animation = "|/-\\"
    anicount = 0
      
    # used to keep the track of
    # the duration of animation
    counttime = 0        
      
    # pointer for travelling the loading string
    i = 0                     
  
    while (counttime != 100):
          
        # used to change the animation speed
        # smaller the value, faster will be the animation
        time.sleep(0.075) 
                              
        # converting the string to list
        # as string is immutable
        load_str_list = list(load_str) 
          
        # x->obtaining the ASCII code
        x = ord(load_str_list[i])
          
        # y->for storing altered ASCII code
        y = 0                             
  
        # if the character is "." or " ", keep it unaltered
        # switch uppercase to lowercase and vice-versa 
        if x != 32 and x != 46:             
            if x>90:
                y = x-32
            else:
                y = x + 32
            load_str_list[i]= chr(y)
          
        # for storing the resultant string
        res =''             
        for j in range(ls_len):
            res = res + load_str_list[j]
              
        # displaying the resultant string
        sys.stdout.write("\r"+res + animation[anicount])
        sys.stdout.flush()
  
        # Assigning loading string
        # to the resultant string
        load_str = res
  
          
        anicount = (anicount + 1)% 4
        i =(i + 1)% ls_len
        counttime = counttime + 1
    print("")
    
  
# # Driver program
# if __name__ == '__main__': 
#     load_animation()
        
        
def statblock():
    print("__________________________")
    print("Location: " + at)
    print("Married: " + str(married))
    print("Started: " + str(started))
    print("Day: " + day)
    print("Time: " + timehour)
    print("Natural Time Pass: " + str(naturaltimepass))
    print("Have food with you:" + str(havefood))
    print("Hunger: " + str(hunger))
    print("Food at home: " + str(homefood))
    print("Money: " + str(money))
    print("Car Version: " + carver)
    print("__________________________")
    
def death():
    for i in range(50):
        print("")
        time.sleep(.05)
    #load_animationdeath()
    global started
    global at
    global hour
    global nextday
    global day
    global naturaltimepass
    global married
    global dstatsettings
    global dstatstartup
    global dstatprompt
    global displaystats
    global homefood
    global timehour
    global tempds
    global crazyval
    global money
    global foodchoice
    global havefood
    global homefood
    global hunger
    global foodisfries
    global car
    car = False
    started = False
    at = "Home"
    married = False
    day = "Monday"
    havefood = False
    hunger = 100
    naturaltimepass = True
    hour = 6
    timehour = ""
    nextday = False
    dstatsettings = False
    dstatstartup = True
    dstatprompt = False
    displaystats = ""
    homefood = 0
    foodisfries = False
    tempds = 0
    money = 0
    crazyval = 0
    foodchoice = 0
    car = True
    time.sleep(1.5)
    print("All stats have been reset")
    time.sleep(1.5)
    for i in range(50):
        print("")
        time.sleep(.05)
    if dstatstartup == True:
        statblock()
        time.sleep(4)
    
        
        
def load_animationdeath():
  
    # String to be displayed when the application is loading
    load_str = "you died"
    ls_len = len(load_str)
  
  
    # String for creating the rotating line
    animation = "Xx"
    anicount = 0
      
    # used to keep the track of
    # the duration of animation
    counttime = 0        
      
    # pointer for travelling the loading string
    i = 0                     
  
    while (counttime != 100):
          
        # used to change the animation speed
        # smaller the value, faster will be the animation
        time.sleep(0.035) 
                              
        # converting the string to list
        # as string is immutable
        load_str_list = list(load_str) 
          
        # x->obtaining the ASCII code
        x = ord(load_str_list[i])
          
        # y->for storing altered ASCII code
        y = 0                             
  
        # if the character is "." or " ", keep it unaltered
        # switch uppercase to lowercase and vice-versa 
        if x != 32 and x != 46:             
            if x>90:
                y = x-32
            else:
                y = x + 32
            load_str_list[i]= chr(y)
          
        # for storing the resultant string
        res =''             
        for j in range(ls_len):
            res = res + load_str_list[j]
              
        # displaying the resultant string
        sys.stdout.write("\r"+res + animation[anicount])
        sys.stdout.flush()
  
        # Assigning loading string
        # to the resultant string
        load_str = res
  
          
        anicount = (anicount + 1)% 4
        i =(i + 1)% ls_len
        counttime = counttime + 1
    print("")
        