import Tkinter, os, csv, sys, shutil, os.path
from tkFileDialog import askdirectory
from pygame import mixer
from Tkinter import *
import tkMessageBox

dirname = '!'
settings = [[]]
dirSet = 0
active = []
mixer.init()
sounda = ''

def dialErrMsg(title, content, quitOut):
    tkMessageBox.showinfo(title, content)
    if quitOut:
        top.destroy()

#For if the installer screws up
if( not os.path.isfile(os.getcwd() + '/settings.txt')):
    os.chdir(os.getcwd() + '/../')

#For if the shortcut screws up
if(not os.path.isfile(os.getcwd() + '/settings.txt')):
    while 1:
        dialErrMsg('Locate', 'Locate the Dota Sound Modder folder', 0)
        dirname = askdirectory()
        os.chdir(dirname)
        if(os.path.isfile(os.getcwd() + '/settings.txt')):
            break

def playSound(index):
    global sounda, settings, active
    mixer.music.stop()
    if active[index].get() != -1:
        sounda = mixer.music.load(open(os.getcwd() + '\\sounds\\' + settings[active[index].get()][2],'rb'))
        mixer.music.play()
        
def getSteamDir():
    global dirname, dirSet
    dirname = askdirectory()
    while(not os.path.exists(dirname)):
        if dirname == '':
          break
        dialErrMsg("Error", "Cannot open that directory!", 0)
        dirname = askdirectory()
    if dirname == '':
        dirSet = 0
        return
    dirname = dirname + "/SteamApps/common/dota 2 beta/dota"
    if(not os.path.exists(dirname)):
        dirSet = 0
        dialErrMsg("Cannot find Dota 2", "Dota 2 is either not installed or important files are missing. Reinstall/verify game cache", 0)
    else:
        dirSet = 1
        
                          
def readFiles():
    global settings, active
    i = 0
    j = 0
    try:
        file = csv.reader(open(os.getcwd() + '/settings.txt', 'rb'), delimiter=',')
    except Exception:
        dialErrMsg("Opening file", "Cannot open file", 1)
    for row in file:
        if row == "\n":
            continue
        for column in row:
            if i == 0:
                j+= 1
        i+= 1
    settings = [['' for x in range(j)] for x in range(i)]
    active = [-1 for x in range(i)]
    try:
        file = csv.reader(open(os.getcwd() + '/settings.txt', 'rb'), delimiter=',')
    except Exception:
        dialErrMsg("Opening file", "Cannot open file", 1)
    i = 0
    j = 0
    for row in file:
        for column in row:
            settings[i][j] = column
            j+= 1
        j = 0
        i+= 1

def submitForms():
    global active, dirSet, settings, dirname
    if dirSet == 0:
        dialErrMsg("No directory set", "Please select your steam directory", 0)
        return
    #Add display for already existant files
    string = "Added: "
    for index in active:
        if index.get() != -1:
            if not os.path.isfile(dirname+ '/' + settings[index.get()][1] + settings[index.get()][2]):
                try:
                    os.makedirs(settings[index.get()][1])
                except Exception:
                    pass
                shutil.copy(os.getcwd() + '/sounds/' + settings[index.get()][2], dirname + '/' + settings[index.get()][1])
            string = string + settings[index.get()][2] + ', '

    string = string[:-2]
    dialErrMsg("Added Sounds", string, 0)

    
    

def removeForms():
    global active, dirSet, settings, dirname
    if dirSet == 0:
        dialErrMsg("No directory set", "Please select your steam directory", 0)
        return
    #Add display for non existant files
    string = "Removed: "
    for index in active:
        if index.get() != -1:
            if os.path.isfile(dirname + '/' + settings[index.get()][1] + settings[index.get()][2]):
                os.remove(dirname + '/' + settings[index.get()][1] + settings[index.get()][2])
            string = string + settings[index.get()][2] + ', '

    string = string[:-2]
    dialErrMsg("Removed Sounds", string, 0)      
        
    

top = Tkinter.Tk()
top.title("Dota 2 Sound Installer")
readFiles()
w = 393
h = 82
sw = top.winfo_screenwidth()
sh = top.winfo_screenheight()
i = 0
while(h < sh - 100 and i < len(settings)):
    h+= 28
    i+= 1
x = (sw - w) / 2
y = (sh - h) / 2
top.geometry("%dx%d+%d+%d" % (w, h, x, y))

a = Tkinter.Button(top, width=55, height="2", text="Locate Steam Directory", command = lambda: getSteamDir()).grid(row = 0, columnspan=2, column = 0)
c = Tkinter.Button(top, width=55, height="2", text="Exit", command = lambda: top.destroy()).grid(row = 2, columnspan=2, column = 0)
e = Tkinter.Label(top, width=55, height="2", text="Custom Sounds:").grid(row = 2, columnspan=2, column = 0)
i = 0
for name in settings:
    active[i] = IntVar()
    active[i].set(-1)
    Tkinter.Checkbutton(top, width=24, height=2, text=name[0], variable=active[i], onvalue=i, offvalue='-1', command =lambda i=i:playSound(i)).grid(row = (3 + i/2), column = i%2)
    i+= 1
d = Tkinter.Button(top, width=27, height="2", text="Submit", command = lambda: submitForms()).grid(row= 4 + i/2, columnspan=1, column = 0)
f = Tkinter.Button(top, width=27, height="2", text="Remove", command = lambda: removeForms()).grid(row = 4 + i/2, columnspan=1, column = 1)
top.mainloop()



