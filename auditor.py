import Tkinter
import string
import subprocess
import time
from Tkinter import *
#from subprocess import call
#from collections import defaultdict

            #Requires whois by Mark Russinovich:
#http://technet.microsoft.com/en-us/sysinternals/bb897435.aspx

#using the documentation from:
#http://www.tutorialspoint.com/python/python_gui_programming.htm

#########################################################
#begin window layout


#initialize a Tk window, in this case our root window
main = Tkinter.Tk()
frame = Frame(main)
frame.pack()

#Define a frame for the Reference server name/ip
referenceserverframe = Frame(main)
referenceserverframe.pack(side=TOP)

#Define a frame for the Target server name/ip
targetserverframe = Frame(main)
targetserverframe.pack(side=TOP)

#Define a frame for the Open File/Path
openfileframe = Frame(main)
openfileframe.pack(side=TOP)

#Define a frame for the Open File/Path
savefileframe = Frame(main)
savefileframe.pack(side=TOP)

#Define a frame for the results of nslookup on the left side of the window
nslookupframe = Frame(main)
nslookupframe.pack(side=LEFT)

#Define a frame for the results of whois on the right side of the window
whoisframe = Frame(main)
whoisframe.pack(side=LEFT)

##########################################################
#initialize a host entry box, label

#initialize a variable to hold the textbox entry
hostName = StringVar()
#Generates a field for the entry of ip address/addresses
hostNameField = Entry(frame, textvariable=hostName)
#generate a geometric box around your object and place it
hostNameField.pack(side=LEFT)

#create a label to the left of the host entry box
hostNamelabelstring = StringVar()
hostNamelabelstring.set("Hostname or single IP")
hostNamelabel = Label(frame, textvariable=hostNamelabelstring)
hostNamelabel.pack(side=LEFT)

############################################################
#initalize a open file path input box, label

#initialize a variable to hold the textbox entry
openFilePath = StringVar()
#initialize things
openFilePath.set("c:/util/hosts.txt")
#generates a field for the entry of filename/path
openFilePathField = Entry(openfileframe, textvariable=openFilePath, width=55)
#generate a geometric box around your object and place it
openFilePathField.pack(side=LEFT)

#create a label to the left of the host entry box
openFileLabelString = StringVar()
openFileLabelString.set("Enter an import filename")
openFileLabel = Label(openfileframe, textvariable=openFileLabelString)
openFileLabel.pack(side=LEFT)

###########################################################
#initialize a save file path input box, label

#initialize a variable to hold the textbox entry
saveFilePath = StringVar()
#initialize things
saveFilePath.set("c:/util/hostResults.txt")
#generates a filed for the entry of filename/path
saveFilePathField = Entry(savefileframe, textvariable=saveFilePath, width=55)
#generate a geometric box around your object and place it
saveFilePathField.pack(side=LEFT)

#create a label to the left of the save file path entry box
saveFileLabelString = StringVar()
saveFileLabelString.set("Enter a save filename")
saveFileLabel = Label(savefileframe, textvariable=saveFileLabelString)
saveFileLabel.pack(side=LEFT)

############################################################
#initialize a host entry box, label

#initialize a variable to hold the textbox entry
referenceServerName = StringVar()
#initialize things
referenceServerName.set("208.72.105.3")
#Generates a field for the entry of ip address/addresses
referenceServerNameField = Entry(referenceserverframe, textvariable=referenceServerName)
#generate a geometric box around your object and place it
referenceServerNameField.pack(side=LEFT)

#Create a label to the left of the host entry box
referenceServerNamelabelstring = StringVar()
referenceServerNamelabelstring.set("Reference Server (always recursive)")
referenceServerNamelabel = Label(referenceserverframe, textvariable=referenceServerNamelabelstring)
referenceServerNamelabel.pack(side=LEFT)

############################################################
#initialize a host entry box, label

#initialize a variable to hold the textbox entry
targetServerName = StringVar()
#initialize things
targetServerName.set("ns.ori.net")
#Generates a field for the entry of ip address/addresses
targetServerNameField = Entry(targetserverframe, textvariable=targetServerName)
#generate a geometric box around your object and place it
targetServerNameField.pack(side=LEFT)

#create a label to the left of the host entry box
targetServerNamelabelstring = StringVar()
targetServerNamelabelstring.set("Target Server (usually authoritative)")
targetServerNamelabel = Label(targetserverframe, textvariable=targetServerNamelabelstring)
targetServerNamelabel.pack(side=LEFT)

#############################################################
#Add a fucking Scrollbar
scrollbar = Scrollbar(whoisframe)
scrollbar.pack(side=RIGHT, fill=Y)


##############################################################
#initialize results pane for WHOIS

#initialize a variable to hold the textbox entry, and bind the length of the scrollbar
#to the length of the whois results frame
whoisResults = Text(whoisframe, yscrollcommand=scrollbar.set, height=25, width=70)
whoisResults.pack(side=LEFT)

##############################################################
#bind scrollbar to things
scrollbar.configure(command=whoisResults.yview)


#################################################################################
#Define a function to load the contents of a file by iterating over each line filling a list


def loadhosts():
    hostlist = []
    with open(openFilePath.get(), 'r', 0) as f:
        for line in f:
            hostlist.append(line)
    f.close()
    return hostlist

################################################################################
#Define a function to write the results of a process to a file line by line


def savewhoisresults():
    results = lookupwhoiesults()
    with open(str(saveFilePath.get()), 'w') as afile:
        for item in results:
            afile.write(str(item))
#################################################################################
#Define a function to load the contents of a file one line at a time into the results screen


def showhosts():
    whoisResults.delete("1.0", END)
    a = loadhosts()
    for i in a:
        whoisResults.insert(INSERT, i)


################################################################################
#The following function will preform the actions specified by checkHost,
#looks up with whois the things in the textbox upon clicking the button.
#Then, we declare the button
################################################################################
#Thought about rewriting this function, as it only displays
#the last task result. Instead I added batch import/output functionality
#At this point I decided the main gui is for one-off functionality
################################################################################

#Define the nslookup commands to use against the host entered in the host txt field


def checkhost(servername):
    a = HostNameEnum()
    results = []
    for i in a:
        #print(check(str(i)))
        results.append(Check(str(i), servername))
    return results

       # if str(resultslabelstring.get()) == "empty":
       #     resultslabelstring.set(results)
       # else:
       #     resultslabelstring.set(resultslabelstring.get() + results)


#Define the action for the button, including calling checkHost doing an nslookup,
#and load whois into the scroll textbox at the right.


def comparehost():
    resultslabel.delete("1.0", END)
    #resultslabel.insert(INSERT, (checkhost(str(referenceServerName.get()))))
    for i in checkhost(str(referenceServerName.get())):
        resultslabel.insert(INSERT, i)
    #resultslabel.insert(INSERT, (checkhost(str(targetServerName.get()))))
    for i in checkhost(str(targetServerName.get())):
        resultslabel.insert(INSERT, i)
    #checkhost(str(referenceServerName.get()))
    #checkhost(str(targetServerName.get()))
    #add the whois function call
    #whoisResults.insert(
    #print(whois(str(hostName.get())))
    whoisResults.delete("1.0", END)
    whoisResults.insert(INSERT, (Whois(str(hostName.get()))))
#call compareHost on button click
#object = Widget(Windoname, text=window title, command=function to call, optional things)

#Declare a button, and give it as "command=blah" the function name you wish to call
hostNameCheck = Button(frame, text='check', command=comparehost)

#generate a geometric box around your object and place it
hostNameCheck.pack(side=TOP)

#############################################################
#Add a fucking Scrollbar
scrollbarnslookup = Scrollbar(nslookupframe)
scrollbarnslookup.pack(side=RIGHT, fill=Y)

#Declare a new label for the results

#resultslabelstring = StringVar()
#resultslabelstring.set("empty")
resultslabel = Text(nslookupframe, yscrollcommand=scrollbarnslookup.set, height=25, width=35)
resultslabel.pack(side=TOP)

#########################################################################
#The following function gets the hosts file loaded and ready to parse
#then, we define a openFileButton

#Declare a button, and give it as "command=blah" the function name you wish to call
openFileButton = Button(openfileframe, text='Load', command=showhosts)

#generate a geometric box around your object and place it
openFileButton.pack(side=TOP)


#########################################################
#end of window layout
#########################################################

#create a class to instantiate a command line, passing arguments to the object


class CommandLine:
    
        """ Parses a command list formatted thusly:
        ['ping', '-c', '4', 'ip address']
        for command line usage, parameterizes two
        strings and standard output is string out, and err"""
        
        #calling commandline with a command will return 2 vars:
        #self.out and self.err, the result of mapping stdout
        #and stderr is a string
        
        def __init__(self, args):
            #Fist, let's pick up the arguments and define a method of using them
            self.args = args
            #next, let's spawn a process using self.args, and piping the IO
            proc = subprocess.Popen(self.args, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE,
                                    creationflags=subprocess.SW_HIDE, shell=True)
            #finally, set self.out and self.error to stderr and stdout
            self.out, self.err = proc.communicate()
            
            #calling commandline with a command will return 2 vars:
            #self.out and self.err, the result of mapping
            #stdout and stderr is a string
        
        #now, let's provide output of the command as a string
        def __str__(self):
            #This is a trainwreck - it returns either error or result of checking
            return str(self.out)

#Inherit from the commandline class, and use it to do an nslookup using the specified parameters


class Check(CommandLine):
    
        """ checks a host"""
        
        def __init__(self, host, server):
            self.host = host
            self.server = server
        
        def __repr__(self):
            self.out = CommandLine(['nslookup', self.host, self.server]).out
            return self.out
        
        def __str__(self):
            self.out = CommandLine(['nslookup', self.host, self.server]).out
            return str(self.out)
            
#Inherit from the commandline class, and use it to do a whois lookup using the specified parameters


class Whois(CommandLine):
    
        """ checks a host"""
        
        def __init__(self, host):
            self.host = host
        
        def __repr__(self):
            self.out = CommandLine(['whois', '-v', self.host]).out
            return self.out
        
        def __str__(self):
            self.out = CommandLine(['whois', '-v', self.host]).out
            return str(self.out)
            
#class to take an ip or a range, and either do something useful, or iterate
#and die trying

################################################################################
#TODO:  Horrible bug, if you start from the middle of a range, and add 1
#for example "192.168.1.11-15" you get check(192.168.1.1-25) results, WTF!!
################################################################################


class HostNameEnum:
    #gets the host from a text input field
    def __init__(self):
        self.hostName = hostName.get()
        self.hostList = []
        self.tempHost = []
        
        #would be shocked if this works at all right out of the gate:
        if len(string.split(self.hostName, sep=";")) > 1:
            for i in range(0, len(self.hostName)):
                self.tempHost = string.split(str(self.hostName), sep=";")[1]
                self.hostList.append(self.tempHost)
        else:
            self.hostList.append(self.hostName)

    def __repr__(self):
        return list.self.hostList
        
    def __str__(self):
        return str(self.hostList)

    def __getitem__(self, i):
        return str(self.hostList[i])

#######################################################################
#TODO: Finish Writing savewhoisresults function


def lookupwhoiesults():
    results = []
    whoisResults.delete("1.0", END)
    a = loadhosts()
    for i in a:
        time.sleep(12)
        results.append(Whois(str.split(i)[0]))
        #print results
        whoisResults.insert(INSERT, results)
    return results

#########################################################################
#The following function gets the hosts file loaded and ready to parse
#then, we define a savewhoisresults button

#Declare a button, and give it as "command=blah" the function name you wish to call
whoisFileButton = Button(savefileframe, text='Whois', command=savewhoisresults)

#generate a geometric box around your object and place it
whoisFileButton.pack(side=TOP)


#########################################################
#call window!

main.mainloop()
