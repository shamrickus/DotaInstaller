import Tkinter, os, csv, sys
from tkFileDialog import askdirectory
from pygame import mixer
from Tkinter import *
import tkMessageBox

dirname = '!'
settings = [[]]
dirSet = 0
active = []
#pygame.init()
mixer.init()
sounda = ''


def dialErrMsg(title, content, quitOut):
    tkMessageBox.showinfo(title, content)
    if quitOut:
        top.destroy()

def playSound(name):
    global sounda, settings, active
    i = 0
    print name
    for names in settings:
        if names[0] == name:
            index = i
            break;
        i+= 1
    print active[index].get()
    mixer.music.pause()
    if active[index].get() != -1:
        print os.getcwd() + '\\sounds\\' + settings[active[index].get()][2]
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
    if(not os.path.exists(dirname + "/SteamApps/common/dota 2 beta/dota")):
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
    global active, dirSet, settings
    if dirSet == 0:
        dialErrMsg("No directory set", "Please select your steam directory", 0)
        return

    print active
    for name in active:
        print name.get()
    

top = Tkinter.Tk()
top.title("Dota 2 Sound Installer")
readFiles()
w = 366
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

a = Tkinter.Button(top, width=51, height="2", text="Locate Steam Directory", command = lambda: getSteamDir()).grid(row = 0, columnspan=2, column = 0)
c = Tkinter.Button(top, width=51, height="2", text="Exit", command = lambda: top.destroy()).grid(row = 2, columnspan=2, column = 0)
e = Tkinter.Label(top, width=51, height="2", text="Custom Sounds:").grid(row = 2, columnspan=2, column = 0)
i = 0
for name in settings:
    active[i] = IntVar()
    active[i].set(-1)
    Tkinter.Checkbutton(top, width=22, height=2, text=name[0], variable=active[i], onvalue=i, offvalue='-1', command =lambda:playSound(name[0])).grid(row = (3 + i/2), column = i%2)
    i+= 1
d = Tkinter.Button(top, width=51, height="2", text="Submit", command = lambda: submitForms()).grid(row= 4 + i/2, columnspan=2, column = 0)

top.mainloop()



