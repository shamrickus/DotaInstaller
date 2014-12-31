import Tkinter, os, csv, sys, shutil, os.path
from tkFileDialog import askdirectory
from pygame import mixer
from Tkinter import *
import tkMessageBox

#Contains the path to the dota folder
dirname = '!'
#Contains all the custom file details
#settings[x][0] File Name for Displaying
#settings[x][1] Destination
#settings[x][2] File Name
#settings[x][3] File Type
#settigns[x][4-6] Repeat index 1-3 for corresponding
#file such as a script
settings = [[]]
#If a correct steam directory has been found
dirSet = 0
#Tracks which files to be installed/deleted
#if the value for a given index is -1, it is unchecked
active = []
#Initializing sound bits
mixer.init()
sounda = ''

#Displays a dialog with the given title and content, if quitOut is true, terminate tkinter
def dialErrMsg(title, content, quitOut):
    tkMessageBox.showinfo(title, content)
    if quitOut:
        top.destroy()


#For if the installer screws up
#if( not os.path.isfile(os.getcwd() + '/settings.txt')):
#    os.chdir(os.getcwd() + '/../')

#If installer.py is not in the same directory as settings (and sounds/scripts)
#then ask the user to locate the folder
if(not os.path.isfile(os.getcwd() + '/settings.txt')):
    while not os.path.isfile(os.getcwd() + '/settings.txt')):
        dialMsg('Locate', 'Locate the Dota Sound Modder folder', 0)
        dirname = askdirectory()
        os.chdir(dirname)

#TODO: Volume management?
#Plays sound with the given checkbox index
def playSound(index):
    global sounda, settings, active
    mixer.music.stop()
    if active[index].get() != -1:
        sounda = mixer.music.load(open(os.getcwd() + '\\sounds\\' + settings[active[index].get()][2],'rb'))
        mixer.music.play()

#Prompting user for the steam directory location
def getSteamDir():
    global dirname, dirSet
    dirname = askdirectory()
    while(not os.path.exists(dirname)):
        #Scenario in which user presses cancel
        if dirname == '':
          break
        dialMsg("Error", "Cannot open that directory!", 0)
        dirname = askdirectory()
    if dirname == '':
        dirSet = 0
        return
    dirname = dirname + "/SteamApps/common/dota 2 beta/dota"
    if(not os.path.exists(dirname)):
        dirSet = 0
        dialMsg("Cannot find Dota 2", "Dota 2 is either not installed or important files are missing. Reinstall/verify game cache", 0)
    else:
        dirSet = 1
        
#Filling settings array with data from settings.txt                          
def readFiles():
    global settings, active
    i = 0
    j = 0
    try:
        file = csv.reader(open(os.getcwd() + '/settings.txt', 'rb'), delimiter=',')
    except Exception:
        dialMsg("Opening file", "Cannot open settings.txt", 1)
    #Getting the size of the data for allocation
    for row in file:
        #Ignoring blank lines
        if row == "\n":
            continue
        for column in row:
            if i == 0:
                j+= 1
        i+= 1
    settings = [['' for x in range(j)] for x in range(i)]
    active = [-1 for x in range(i)]
    
    i = 0
    j = 0
    try:
        file = csv.reader(open(os.getcwd() + '/settings.txt', 'rb'), delimiter=',')
    except Exception:
        dialMsg("Opening file", "Cannot open settings.txt", 1)
    #filling the settings array
    for row in file:
        for column in row:
            settings[i][j] = column
            j+= 1
        j = 0
        i+= 1

#TODO: Also copy the script over
#      elegently append script/handle mutiple files adding to one scritpt
#Adding selected files
def addFiles():
    global active, dirSet, settings, dirname
    if dirSet == 0:
        dialMsg("No directory set", "Please select your steam directory", 0)
        return
    #TODO: Add display for already existant files
    string = "Added: "
    for index in active:
        if index.get() != -1:
            #If the file does not already exist
            if not os.path.isfile(dirname+ '/' + settings[index.get()][1] + settings[index.get()][2]):
                try:
                    os.makedirs(settings[index.get()][1])
                except Exception:
                    #The directories already exist or we don't have permission
                    pass
                try:
                    shutil.copy(os.getcwd() + '/sounds/' + settings[index.get()][2], dirname + '/' + settings[index.get()][1])
                    #Appending string for displaying what was added
                    string = string + settings[index.get()][2] + ', '
                #TODO: Display error to user
                except Exception:
                    #Cannot copy file 
                    pass
    #Trimming trailing ', '
    string = string[:-2]
    dialMsg("Added Sounds", string, 0)

    
    

def removeFiles():
    global active, dirSet, settings, dirname
    if dirSet == 0:
        dialMsg("No directory set", "Please select your steam directory", 0)
        return
    #TODO: Add display for non existant files
    string = "Removed: "
    for index in active:
        if index.get() != -1:
            #If the file exists
            if os.path.isfile(dirname + '/' + settings[index.get()][1] + settings[index.get()][2]):
                try:
                    os.remove(dirname + '/' + settings[index.get()][1] + settings[index.get()][2])
                    string = string + settings[index.get()][2] + ', '
                #TODO: Display error to user
                except Exception:
                    #Cannot delete file
                    pass
    #Trimming trailing ', '
    string = string[:-2]
    dialMsg("Removed Sounds", string, 0)      
        
    

top = Tkinter.Tk()
top.title("Dota 2 Sound Installer")
readFiles()
#Default window size
w = 393
h = 82
sw = top.winfo_screenwidth()
sh = top.winfo_screenheight()
i = 0
#Increasing window height based on how many checkboxes there are
while(h < sh - 100 and i < len(settings)):
    h+= 28
    i+= 1
#centering the screen
x = (sw - w) / 2
y = (sh - h) / 2
top.geometry("%dx%d+%d+%d" % (w, h, x, y))
#Adding buttons
loc = Tkinter.Button(top, width=55, height="2", text="Locate Steam Directory", command = lambda: getSteamDir()).grid(row = 0, columnspan=2, column = 0)
exit = Tkinter.Button(top, width=55, height="2", text="Exit", command = lambda: top.destroy()).grid(row = 2, columnspan=2, column = 0)
lab = Tkinter.Label(top, width=55, height="2", text="Custom Sounds:").grid(row = 2, columnspan=2, column = 0)
i = 0
for name in settings:
    active[i] = IntVar()
    active[i].set(-1)
    Tkinter.Checkbutton(top, width=24, height=2, text=name[0], variable=active[i], onvalue=i, offvalue='-1', command =lambda i=i:playSound(i)).grid(row = (3 + i/2), column = i%2)
    i+= 1
add = Tkinter.Button(top, width=27, height="2", text="Add", command = lambda: addFiles()).grid(row= 4 + i/2, columnspan=1, column = 0)
rem = Tkinter.Button(top, width=27, height="2", text="Remove", command = lambda: removeFiles()).grid(row = 4 + i/2, columnspan=1, column = 1)
top.mainloop()



