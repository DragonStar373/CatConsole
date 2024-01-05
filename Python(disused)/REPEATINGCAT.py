import time





#da stuff
def rcat():
    while True:
        print("REPEATING CAT")
        print("!!!\n")
        fox = input("meow?:")
        if fox.lower() == "quit" or fox.lower() == "exit":
            break
        if fox.lower() == "help":
            print("its a repeating cat. its self explanitory.")
        if fox.lower() == "meow":
            for i in range(20):
                print("meow")
                time.sleep(.1)
        if fox.lower() != "meow":
            print("")
        print(fox + "\n")
        time.sleep(1)