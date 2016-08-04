from time import sleep
import random

with open("../json/exampleSigData.json") as json:
    jlist = json.read()

jlist = jlist.strip()[1:len(jlist)-1]

jlist = jlist.split("},")

for index, thing in enumerate(jlist):
    jlist[index] = thing + "}"

jlist = jlist[:len(jlist)-1]

for thing in jlist:
    print(thing)

while(True):
    x = random.randint(0, len(jlist) - 1)
    #with open("/Applications/MAMP/htdocs/jason.json","w") as json:
    with open("../json/jason.json", "w") as json:
        json.write(jlist[x])

#print("Test")
    sleep(5)
