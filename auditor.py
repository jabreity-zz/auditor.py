import Tkinter
import string
import subprocess
from Tkinter import *
from subprocess import call
from collections import defaultdict



#Requires whois by Mark Russinovich:
#http://technet.microsoft.com/en-us/sysinternals/bb897435.aspx

#using the documentation from:
#http://www.tutorialspoint.com/python/python_gui_programming.htm
#########################################################
#begin window layout


#initialize a Tk window
main = Tkinter.Tk()
frame = Frame(main)
frame.pack()

middleframe = Frame(main)
middleframe.pack(side=TOP)

middle1frame = Frame(main)
middle1frame.pack(side=TOP)

bottomframe = Frame(main)
bottomframe.pack(side=LEFT)

bottomframe1 = Frame(main)
bottomframe1.pack(side=LEFT)

##########################################################
#initialize a host entry box, label, and action button

#initialize a variable to hold the textbox entry
hostName = StringVar()
#Generates a field for the entry of ip address/addresses
hostNameField = Entry(frame, textvariable=hostName)
#generate a geometric box around your object and place it
hostNameField.pack(side = LEFT)

hostNamelabelstring = StringVar()
hostNamelabelstring.set("Hostname or single IP")
hostNamelabel = Label(frame, textvariable=hostNamelabelstring)
hostNamelabel.pack(side = LEFT)

############################################################
#initialize a host entry box, label, and action button

#initialize a variable to hold the textbox entry
referenceServerName = StringVar()
#initialize things
referenceServerName.set("208.72.105.3")
#Generates a field for the entry of ip address/addresses
referenceServerNameField = Entry(middleframe, textvariable=referenceServerName)
#generate a geometric box around your object and place it
referenceServerNameField.pack(side = LEFT)

referenceServerNamelabelstring = StringVar()
referenceServerNamelabelstring.set("Reference Server (always recursive)")
referenceServerNamelabel = Label(middleframe, textvariable=referenceServerNamelabelstring)
referenceServerNamelabel.pack(side = LEFT)

############################################################
#initialize a host entry box, label, and action button

#initialize a variable to hold the textbox entry
targetServerName = StringVar()
#initialize things
targetServerName.set("ns.ori.net")
#Generates a field for the entry of ip address/addresses
targetServerNameField = Entry(middle1frame, textvariable=targetServerName)
#generate a geometric box around your object and place it
targetServerNameField.pack(side = LEFT)

targetServerNamelabelstring = StringVar()
targetServerNamelabelstring.set("Target Server (usually authoritative)")
targetServerNamelabel = Label(middle1frame, textvariable=targetServerNamelabelstring)
targetServerNamelabel.pack(side = LEFT)

#############################################################
#Add a fucking Scrollbar
scrollbar = Scrollbar(bottomframe1)
scrollbar.pack(side=RIGHT, fill=Y)


##############################################################
#initialize results pane for WHOIS

#initialize a variable to hold the textbox entry
whoisResults = Text(bottomframe1)
whoisResults.pack(side=LEFT)

##############################################################
#bind scrollbar to things
scrollbar.configure(command=whoisResults.yview)


#looks up with whois the things in the textbox upon clicking the button

################################################################################
#TODO: Rewrite this function, it's got a nasty implementation, where it only displays
#the last ping task result.  *sigh* only so much time in the day.
################################################################################


def checkHost(serverName):
    #print hostNameEnum(hostName.get())
    #a = hostNameEnum()
    #for i in a:
    #    print i
    a = hostNameEnum()
    
    for i in a:
        #print(check(str(i)))
        results = str(check(str(i), serverName))
        if str(resultslabelstring.get()) == "empty":
            resultslabelstring.set(results)
        else:
            resultslabelstring.set(resultslabelstring.get() + results)

def compareHost():
    resultslabelstring.set("empty")
    checkHost(str(referenceServerName.get()))
    checkHost(str(targetServerName.get()))
    #add the whois function call
    #whoisResults.insert(
    #print(whois(str(hostName.get())))
    whoisResults.delete("1.0", END)
    whoisResults.insert(INSERT, (whois(str(hostName.get()))))
#call compareHost on button click
#object = Widget(Windoname, text=window title, command=function to call, optional things)
hostNameCheck = Button(frame, text='check', command=compareHost)

#generate a geometric box around your object and place it
hostNameCheck.pack(side = TOP)

resultslabelstring = StringVar()
resultslabelstring.set("empty")
resultslabel = Label(bottomframe, textvariable=resultslabelstring, height=45, width = 60)
resultslabel.pack(side = TOP)

#########################################################
#end of window layout
#########################################################

#create a class to instantiate a command line, passing arguments to the object

class commandline:
    
        ''' Parses a command list formatted thusly:
        ['ping', '-c', '4', 'ip address']
        for command line usage, parameterizes two
        strings and standard output is string out, and err'''
        
        #calling commandline with a command will return 2 vars:
        #self.out and self.err, the result of mapping stdout
        #and stderr is a string
        
        def __init__(self, args):
            #Fist, let's pick up the arguments and define a method of using them
            self.args = args
            #next, let's spawn a process using self.args, and piping the IO
            proc = subprocess.Popen(self.args, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.SW_HIDE, shell=True)
            #finally, set self.out and self.error to stderr and stdout
            self.out, self.err = proc.communicate()
            
            #calling commandline with a command will return 2 vars:
            #self.out and self.err, the result of mapping
            #stdout and stderr is a string
        
        #now, let's provide output of the command as a string
        def __str__(self):
            #This is a trainwreck - it returns either error or result of checking
            return str(self.out)


class check(commandline):
    
        ''' checks a host'''
        
        def __init__(self, host, server):
            self.host = host
            self.server = server
        
        def __repr__(self):
            self.out = commandline(['nslookup', self.host, self.server]).out
            return self.out
        
        def __str__(self):
            self.out = commandline(['nslookup', self.host, self.server]).out
            return str(self.out)
            

class whois(commandline):
    
        ''' checks a host'''
        
        def __init__(self, host):
            self.host = host
        
        def __repr__(self):
            self.out = commandline(['whois', '-v', self.host]).out
            return self.out
        
        def __str__(self):
            self.out = commandline(['whois', '-v', self.host]).out
            return str(self.out)
            
#class to take an ip or a range, and either do something useful, or iterate
#and die trying

################################################################################
#TODO:  Horrible bug, if you start from the middle of a range, and add 1
#for example "192.168.1.11-15" you get check(192.168.1.1-25) results, WTF!!
################################################################################


class hostNameEnum:
    #gets the host from a text input field
    def __init__(self):
        self.hostName = hostName.get()
        self.hostList = []
        self.tempHost = []
        
        #would be shocked if this works at all right out of the gate:
        if len(string.split(self.hostName, sep=";")) > 1:
            for i in range(0, len(self.hostName)):
                self.tempHost = string.split(str(self.hostName, sep=";")[i])
                self.hostList.append(self.tempHost[i])
        else:
            self.hostList.append(self.hostName)

    def __repr__(self):
        return list.self.hostList
        
    def __str__(self):
        return str(self.hostList)

    def __getitem__(self, i):
        return str(self.hostList[i])


#########################################################
#call window!

main.mainloop()
