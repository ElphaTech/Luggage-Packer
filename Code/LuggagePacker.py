import json
import os
import sys

fileName=sys.argv[1]
input(fileName)
#fileName="{}/{}".format(os.getcwd(),__file__)

try:
    importedJson=open(fileName,"r")
except:
    importedJson=open(fileName,"w")
    importedJson.write(json.dumps({"Name": "Luggage", "Folders": [], "Items": []}))
    importedJson=open(fileName,"r")
Luggage=json.loads(importedJson.read())
importedJson.close()

def saveLuggage():
    importedJson=open(fileName,"w")
    importedJson.write(json.dumps(Luggage))
    importedJson.close()


def printMatchingItems(s,l,p:str="/",m:bool=False): #search term,location,seperator,true if main run
    searchList=[]
    for i in range(len(l["Items"])):
        if s.upper() in l["Items"][i]["Name"].upper():
            searchList.append("{0}: {1}".format(l["Items"][i]["Name"],p))
    for i in range(len(l["Folders"])):
        tempSearchList=printMatchingItems(s,l["Folders"][i],"{0}{1}/".format(p,l["Folders"][i]["Name"]))
        for j in tempSearchList:
            searchList.append(j)
    if m:
        global packstat
        if len(searchList)>0:
            for i in range(len(searchList)):
                print("{}: {}".format(i+1,searchList[i]))
            inputSearch=input("Type number to quick jump to item or enter to get back to your regularly scheduled programming")
            dirstr=str(searchList[int(inputSearch)-1]).split(": ")[1][1:]
            dirlist=dirstr.split("/")[:-1]
            while len(dirlist)!=0:
                for i in range(len(Location[-1]["Folders"])):
                    if Location[-1]["Folders"][i]["Name"]==dirlist[0]:
                        if len(dirlist)==1:
                            if Location[-1]["Folders"][i]["Packed"]!=packstat:
                                if packstat==False:
                                    packstat=True
                                else:
                                    packstat=False
                        Location.append(Location[-1]["Folders"][i])
                        dirlist.pop(0)
        else:
            print("No results found")
    else:
        return searchList

def checkFolderItem(fi):
    if fi=="f":
        return "Folders"
    elif fi=="i":
        return "Items"
    else:
        print("!: Please use f/i to specify folder or item")
        return False

def checkIfOk(findex,fi):
    try:
        findex=int(findex)-1
    except:
        print("!: Not a number")
        return False
    fi=checkFolderItem(fi)
    if fi==False:
        return False
    if findex<len(Location[-1][fi]):
        if findex>=0:
            return True
        else:
            print("!: Number too small")
            return False
    else:
        print("!: Number too big")
        return False

def removeSpaces(s):
    while s[0]==" ":
        s=s[1:]
    while s[-1]==" ":
        s=s[:-1]
    return "{}{}".format(s[0].upper(),s[1:])

Location=[Luggage]
packstat=False
HelpList=[
    "Commands",
    "[f/i] means write f for folder/i for item",
    "[#] means number of folder/item",
    "[name] means name of folder/item",
    "[p/u] means write p for pack/u for unpack",
    "() around one of the above means optional",
    "",
    "",
    "h: Shows help(This)",
    "",
    "s[name]: Searches for item",
    "",
    "cv: Swaps from showing not packed to showing packed and vice-versa",
    "p[f/i][#](,[#]): Packs or unpacks several folders/items",
    "o[p/u](f/i): Packs or unpacks all folders/items/everything",
    "",
    "f[#]: Goes into a folder",
    "u: Goes out of the current folder",
    "",
    "a[f/i][name]: Adds folder/item",
    "d[f/i][#]: Deletes folder/item",
    "r[f/i][#],[name]: Renames folder/item"
]

os.system("clear")

while True:
    if packstat==False:
        print("\n------------------\n{} - Not Packed\nFolders:".format(Location[-1]["Name"]))
    else:
        print("\n------------------\n{} - Packed\nFolders:".format(Location[-1]["Name"]))

    for i in range(len(Location[-1]["Folders"])):
        if Location[-1]["Folders"][i]["Packed"]==packstat:
            print("f{}: {}".format(i+1,Location[-1]["Folders"][i]["Name"]))
    print("Items:")
    for i in range(len(Location[-1]["Items"])):
        if Location[-1]["Items"][i]["Packed"]==packstat:
            print("i{}: {}".format(f"{i+1:02}",Location[-1]["Items"][i]["Name"]))

    input1=input("Type h for help\n> ")
    os.system("clear")

    if input1=="h":
        for i in HelpList:
            print(i)
    elif input1[:1]=="s":
        printMatchingItems(removeSpaces(input1[1:]),Location[-1],"/",True)
    elif input1=="reboot":
        python = sys.executable
        os.execl(python, python, * sys.argv)

    elif input1=="cv":
        if packstat==False:
            packstat=True
        else:
            packstat=False
    elif input1[:1]=="p":
        findex=input1.split(",")
        findex[0]=findex[0][2:]
        fi=input1[1:2]
        for i in range(len(findex)):
            if checkIfOk(findex[i],fi):
                if Location[-1][checkFolderItem(fi)][int(findex[i-1])-1]["Packed"]:
                    Location[-1][checkFolderItem(fi)][int(findex[i-1])-1]["Packed"]=False
                else:
                    Location[-1][checkFolderItem(fi)][int(findex[i-1])-1]["Packed"]=True
    elif input1[:1]=="o":
        if input1[1:2]=="p":
            pu=True
        elif input1[1:2]=="u":
            pu=False
        else:
            print("!: Please use p/u to specify pack or unpack")
            pass
        if len(input1)==2:
            for i in range(len(Location[-1]["Folders"])):
                Location[-1]["Folders"][i]["Packed"]=pu
            for i in range(len(Location[-1]["Items"])):
                Location[-1]["Items"][i]["Packed"]=pu
        elif len(input1)==3 and checkFolderItem(input1[2:3])!=False:
            for i in range(len(Location[-1][checkFolderItem(input1[2:3])])):
                Location[-1][checkFolderItem(input1[2:3])][i]["Packed"]=pu

    elif input1[:1]=="f":
        findex=int(input1[1:])
        if checkIfOk(findex,"f"):
            Location.append(Location[-1]["Folders"][findex-1])

    elif input1=="u":
        if len(Location)>1:
            Location.pop()
        else:
            print("Already in top folder")

    elif input1[:1]=="a":
        if input1[1:2]=="i":
            Location[-1]["Items"].append({"Name":removeSpaces(input1[2:]),"Packed":packstat})
        elif input1[1:2]=="f":
            Location[-1]["Folders"].append({"Name":removeSpaces(input1[2:]),"Packed":packstat,"Folders":[],"Items":[]})
        else:
            print("Please write command:a[f/i][name]")

    elif input1[:1]=="d":
        findex=input1[2:]
        fi=input1[1:2]
        if checkIfOk(findex,fi):
            del Location[-1][checkFolderItem(fi)][int(findex)-1]

    elif input1[:1]=="r":
        spl=input1.split(",")
        findex=spl[0][2:]
        fi=input1[1:2]
        if checkIfOk(findex,fi) and len(spl)>1:
            Location[-1][checkFolderItem(fi)][int(findex)-1]["Name"]=removeSpaces(spl[1])
        elif len(spl)>1:
            print("!: Please use ,[name] to rename")

    saveLuggage()
print("OUT")