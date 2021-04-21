import os
from threading import Thread
import sys
import time
import webbrowser

FILELIST="filelist.txt"
keep=True
filepath='None'
NATION='None'
class bcolors:
    RED = '\u001b[31m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    MAGENTA = '\u001b[35m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#########################################################
################# SUPPORT BLOCK #########################
#########################################################
def getsystem():
        platforms = {
        'linux1' : 'Linux',
        'linux2' : 'Linux',
        'darwin' : 'OS X',
        'win32' : 'Windows'
        }
        if sys.platform not in platforms:
            return sys.platform
        return platforms[sys.platform].lower()

def disclaimer():
	str="This script is just a file parser that is able to parse data from the 2021 facebook leaks.\nYou should NOT use this script to find information about people who did not authorize you.\n i DO NOT assume any responsability on a bad usage of this script."
	print(bcolors.RED+bcolors.BOLD+str+bcolors.END)
	print("\n\n")
	input("Press any key to continue...")
def printName():
	print(bcolors.RED+bcolors.BOLD+"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"+bcolors.END)
	print(bcolors.RED+bcolors.BOLD+"@@ +++++++++++++++++++++++++++++ @@"+bcolors.END)
	print(bcolors.RED+bcolors.BOLD+"@@ DATA PARSER v1.0              @@"+bcolors.END)
	print(bcolors.RED+bcolors.BOLD+"@@ BASED ON FACEBOOK LEAKS 2021  @@"+bcolors.END)
	print(bcolors.RED+bcolors.BOLD+"@@ by FriendlyWizard23           @@"+bcolors.END)
	print(bcolors.RED+bcolors.BOLD+"@@ +++++++++++++++++++++++++++++ @@"+bcolors.END)
	print(bcolors.RED+bcolors.BOLD+"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"+bcolors.END+"\n")

def chooseCountry():
	global filepath
	choices=[]
	counter=0
	clearSTDOUT()
	printName()
	print(bcolors.CYAN+"$$$$$$$$$$$$$$$$$$$$$$$\n"+bcolors.END)
	with open(FILELIST) as f:
		for line in f:
			line=line.rstrip()
			choices.append(line)
			print(bcolors.CYAN+"["+str(counter)+"]"+line+bcolors.END)
			counter+=1
	print(bcolors.CYAN+"\n$$$$$$$$$$$$$$$$$$$$$$$"+bcolors.END)
	print(bcolors.CYAN+"Currently Selected: "+filepath+bcolors.END)
	nation=int(input("Nation: "))
	if(nation<=-2 or nation>=counter):
		chooseCountry()
	if(nation==-1):
		return
	filepath=choices[nation]
	print("\nFile Path changed! Current: "+filepath)
	time.sleep(1)

def animated_loading():
	chars = "/\|"
	for char in chars:
		sys.stdout.write('\r'+'Searching'+char)
		time.sleep(0.4)
		sys.stdout.flush()
def opts():
	print(bcolors.GREEN+"[+]=====================================[+]"+bcolors.END)
	print(bcolors.GREEN+"[+] (0)  Search by name and surname     [+]"+bcolors.END)
	print(bcolors.GREEN+"[+] (1)  Search by phone number         [+]"+bcolors.END)
	print(bcolors.GREEN+"[+] (2)  Search by Surname		[+]"+bcolors.END)
	print(bcolors.GREEN+"[+] (3)  Change Country path            [+]"+bcolors.END)
	print(bcolors.GREEN+"[+] (4)  Print File content	        [+]"+bcolors.END)
	print(bcolors.GREEN+"[+] (-1) Exit program                   [+]"+bcolors.END)
	print(bcolors.GREEN+"[+]=====================================[+]\n"+bcolors.END)
	op=input(bcolors.GREEN+bcolors.BOLD+"[local@finder]: "+bcolors.END)
	return op

def clearSTDOUT():
    st='clear'
    if ("windows" in getsystem()):
        st='cls'
    os.system(st)

def printParsedString(stuff):
	print("###############################################")
	print(bcolors.MAGENTA+bcolors.BOLD+bcolors.UNDERLINE+"NAME: "+bcolors.END+bcolors.MAGENTA+stuff[2]+bcolors.END)
	print(bcolors.MAGENTA+bcolors.BOLD+bcolors.UNDERLINE+"SURNAME: "+bcolors.END+bcolors.MAGENTA+stuff[3]+bcolors.END)
	print(bcolors.MAGENTA+bcolors.BOLD+bcolors.UNDERLINE+"PHONE NUMBER: "+bcolors.END+bcolors.MAGENTA+stuff[0]+bcolors.END)
	print("###############################################\n")


def parseString(line):
	splitted=line.split(":")
	stuff=[]
	for i in splitted:
		if (i!="" and i!="\n"):
			stuff.append(i)
	return stuff

#########################################################
############### END SUPPORT BLOCK #######################
#########################################################

#########################################################
##################### FILE BLOCK ########################
#########################################################

class ThreadedSearchBySurname(Thread):
	def __init__(self,surname):
		super(ThreadedSearchBySurname,self).__init__()
		self.surname=surname
		self.people=[]
	def run(self):
		with open(filepath) as infile:
			for line in infile:
				stuff=parseString(line)
				if(len(stuff)<4):
					continue
				if(self.surname==stuff[3]):
					self.people.append(line)
	def getPeople(self):
		return self.people

class ThreadedSearchByNumber(Thread):
	def __init__(self,number):
		super(ThreadedSearchByNumber,self).__init__()
		self.number=number
		self.people=[]
	def run(self):
		with open(filepath) as infile:
			for line in infile:
				stuff=parseString(line)
				if (len(stuff)<1):
					continue
				if (self.number in stuff[0]):
					self.people.append(line)
	def getPeople(self):
		return self.people

class ThreadedSearchByName(Thread):
	def __init__(self,name,surname):
		super(ThreadedSearchByName,self).__init__()
		self.name=name
		self.surname=surname
		self.people=[]
	def run(self):
		with open(filepath) as infile:
			for line in infile:
				if (self.name in line and self.surname in line):
					self.people.append(line)
	def getPeople(self):
		return self.people

def openLink(people):
	open=0
	maxlen=len(people)
	if (maxlen==0):
		return
	while(open!=-1):
		print(bcolors.WARNING+"Select the number of person to open on browser [-1 to exit]"+bcolors.END)
		open=int(input())
		if(open==-1):
			return
		if(open>maxlen or open<-1):
			print(bcolors.RED+"out of range!"+bcolors.END)
		else:
			person=parseString(people[open-1])
			id=person[1]
			url="https://www.facebook.com/profile.php?id="+id
			webbrowser.open(url)

def personbysurname():
	printName()
	surname=input("\nSurname: ")
	t=ThreadedSearchBySurname(surname)
	t.start()
	clearSTDOUT()
	printName()
	while(t.is_alive()):
		animated_loading()
	print("\n")
	sys.stdout.flush()
	t.join()
	people=t.getPeople()
	counter=1
	if not people:
		print(bcolors.RED+bcolors.BOLD+"\nNo entity Found\n"+bcolors.END)
	else:
		for person in people:
			prs=parseString(person)
			print(bcolors.RED+"PERSON N. "+bcolors.BOLD+str(counter)+bcolors.END)
			counter+=1
			printParsedString(prs)
	open='0'
	openLink(people)
	val=input("Press any key to continue")
	clearSTDOUT()

def personbynumber():
	printName()
	number=input("\nNumber: ")
	t=ThreadedSearchByNumber(number)
	t.start()
	clearSTDOUT()
	printName()
	while(t.is_alive()):
		animated_loading()
	print("\n")
	sys.stdout.flush()
	t.join()
	people=t.getPeople()
	counter=1
	if not people:
		print(bcolors.RED.bcolors.BOLD+"\nNo entity Found\n"+bcolors.END)
	else:
		for person in people:
			prs=parseString(person)
			print(bcolors.RED+"PERSON N. "+bcolors.BOLD+str(counter)+bcolors.END)
			printParsedString(prs)
			counter+=1
	openLink(people)
	val=input("Press any key to continue")
	clearSTDOUT()


def personbyname():
	printName()
	name=input("\nName: ")
	surname=input("\nSurname: ")
	name=name.lower().capitalize()
	surname=surname.lower().capitalize()
	t=ThreadedSearchByName(name,surname)
	t.start()
	clearSTDOUT()
	printName()
	while(t.is_alive()):
		animated_loading()
	print("\n")
	sys.stdout.flush()
	t.join()
	people=t.getPeople()
	counter=1
	if not people:
		print("No entity Found\n")
	else:
		for person in people:
			prs=parseString(person)
			print(bcolors.RED+"PERSON N. "+bcolors.BOLD+str(counter)+bcolors.END)
			printParsedString(prs)
			counter+=1
	openLink(people)
	val=input("Press any key to continue")
	clearSTDOUT()

def printFile():
	clearSTDOUT()
	printName()
	pr='asd'
	while(pr!='yes' and pr!='y' and pr!='no' and pr!='n'):
		clearSTDOUT()
		printName()
		print(bcolors.WARNING+"Printing out the WHOLE file may take a while and CRASH, would you still continue? [y/n]"+bcolors.END)
		pr=input()
		pr=pr.lower()
	if(pr=='n' or pr=='no'):
		return
	try:
		with open(filepath) as infile:
			for line in infile:
				stuff=parseString(line)
				print(stuff)
				time.sleep(0.1)
	except KeyboardInterrupt:
		return
#########################################################
################# END FILE BLOCK ########################
#########################################################

def startchecks():
	if not os.path.isfile(FILELIST):
		print(bcolors.FAIL+"ERROR: file '"+FILELIST+"' does not exist."+bcolors.END)
		exit(-1)
	with open(FILELIST) as infile:
		for line in infile:
			line=line.rstrip()
			print (line)
			if (not os.path.exists(line)):
				print(bcolors.FAIL+"ERROR: One or more paths in '"+FILELIST+"'Does not exist"+bcolors.END)
				exit(-1)
def main():
	startchecks()
	while(True):
		clearSTDOUT()
		printName()
		choice=opts()
		if(filepath =='None' and choice != '-1' and choice !='3'):
			print(bcolors.WARNING+"WARNING: You need to set the nation file first! (option 3)"+bcolors.END)
			time.sleep(2)
			continue
		if(choice=='0'):
			clearSTDOUT()
			personbyname()
		if(choice=='1'):
			clearSTDOUT()
			personbynumber()
		if(choice=='2'):
			clearSTDOUT()
			personbysurname()
		if(choice=='3'):
			choice=chooseCountry()
		if(choice=='4'):
			printFile()
		if(choice=='-1'):
			clearSTDOUT()
			exit(1)

if __name__ == "__main__":
    disclaimer()
    main()
