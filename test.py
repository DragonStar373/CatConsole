bob = "2:file.txt:4::"

print(len(bob.split(":")))

for i in bob.split(":"):
    print(">:" + i)
