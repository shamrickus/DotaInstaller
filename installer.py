import Tkinter, os, csv, sys, shutil, os.path
from tkFileDialog import askdirectory
import pygame.mixer
from PIL import Image
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
pygame.mixer.init()
sounda = ''
#Contains all the checkboxes
checkbox = []

#Enabling checkboxes/buttons/slider
def enableButtons():
    global checkbox, vol, add, rem, dirSet
    if dirSet:
        i = -1
        for index in checkbox:
            i += 1
            checkbox[i].config(state = "normal")
        vol.config(state = "normal")
        add.config(state = "normal")
        rem.config(state = "normal")

#Disabling checkboxes/buttons/slider  
def disableButtons():
    global checkbox, vol, add, rem, dirSet
    if not dirSet:
        i = -1
        for index in checkbox:
            i += 1
            checkbox[i].config(state = "disabled")
        vol.config(state = "disabled")
        add.config(state = "disabled")
        rem.config(state = "disabled")
        

#Displays a dialog with the given title and content, if quitOut is true, terminate tkinter
def dialMsg(title, content, quitOut = 0):
    tkMessageBox.showinfo(title, content)
    if quitOut:
        top.destroy()

#If installer.py is not in the same directory as settings (and sounds/scripts)
#then ask the user to locate the folder
if(not os.path.isfile(os.getcwd() + '/settings.txt')):
    while not os.path.isfile(os.getcwd() + '/settings.txt'):
        dialMsg('Locate', 'Locate the Dota_File_Installer folder you downloaded', 0)
        curDir = askdirectory()
        print os.path.isfile(os.getcwd() + '/settings.txt')
        if(curDir != ''):
            os.chdir(curDir)
        else:
            top.destroy()

#Hooking up the volume slider
def change_vol(_=None):
    global vol
    pygame.mixer.music.set_volume(vol.get())

#Plays sound with the given checkbox index
def playSound(index):
    global sounda, settings, active
    if active[index] != -1:
        active[index] = -1
    else:
        active[index] = index
    pygame.mixer.music.stop()
    if active[index] != -1:
        sounda = pygame.mixer.music.load(open(os.getcwd() + '\\sound\\' + settings[index][2],'rb'))
        pygame.mixer.music.play()

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
        disableButtons()
        return
    dirname = dirname + "/SteamApps/common/dota 2 beta/dota"
    if(not os.path.exists(dirname)):
        dirSet = 0
        dialMsg("Cannot find Dota 2", "Dota 2 is either not installed or important files are missing. Reinstall/verify game cache", 0)
        disableButtons()
    else:
        dirSet = 1
        checkExisting()
        enableButtons()
        
#Filling settings array with data from settings.txt                          
def readFiles():
    global settings, active, checkbox
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
    checkbox = ['black' for x in range(i)]
    
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


#Checking which files already exist and coloring the appropiate color
def checkExisting():
    global settings, dirname, checkbox
    i = -1
    for index in settings:
        i+= 1
        if os.path.isfile(dirname + '/' + settings[i][1] + settings[i][2]):
            if settings[i][4] != '' and os.path.isfile(dirname + '/' + settings[i][4] + settings[i][5]):
                checkbox[i].config(foreground = 'blue')
            elif settings[i][4] == '':
                checkbox[i].config(foreground = 'blue')
            else:
                checkbox[i].config(foreground = 'red')
        else:
            checkbox[i].config(foreground = 'red')

#TODO: elegently append script/handle mutiple files adding to one scritpt
#Adding selected files
def addFiles():
    global active, dirSet, settings, dirname, checkbox
    if dirSet == 0:
        dialMsg("No directory set", "Please select your steam directory", 0)
        return
    string = "Added: "
    i = -1
    for index in active:
        i+= 1
        if active[index] != -1:
            passed = 0
            #If the file does not already exist
            if not os.path.isfile(dirname+ '/' + settings[index][1] + settings[index][2]):
                try:
                    os.makedirs(settings[index][1])
                except Exception:
                    #The directories already exist or we don't have permission
                    pass
                try:
                    shutil.copy(os.getcwd() + '/sound/' + settings[index][2], dirname + '/' + settings[index][1])
                    if not settings[index][4] != '':    
                        string = string + settings[index][2] + ', '
                        checkbox[i].config(foreground = 'blue')
                    passed = 1
                #TODO: Display error to user
                except Exception:
                    #Cannot copy file
                    print "Exception error: %s" % Exception
                    pass
            else:
                if tkMessageBox.askyesno("Overwrite", "File " + settings[index][2] + " already exists, overwrite?"):
                    try:
                        os.remove(dirname + '/' + settings[index][1] + settings[index][2])
                        shutil.copy(os.getcwd() + '/sound/' + settings[index][2], dirname + '/' + settings[index][1])
                        if not settings[index][4] != '':    
                            string = string + settings[index][2] + ', '
                            checkbox[i].config(foreground = 'blue')
                        passed = 1
                    #TODO: Display Error to user
                    except Exception:
                        #Cannot copy file
                        pass
            #Copying the script
            if passed and settings[index][4] != '':
                if not os.path.isfile(dirname + '/' + settings[index][4] + '/' + settings[index][5]):
                    try:
                        os.makedirs(settings[index][4])
                    except Exception:
                        #The directories already exist or we don't have the permission
                        pass
                    try:
                        shutil.copy(os.getcwd() + '/scripts/' + settings[index][5], dirname + '/' + settings[index][4])
                        checkbox[i].config(foreground = 'blue')
                        #Appending string for displaying what was added
                        string = string + settings[index][2] + ', '
                        string = string + settings[index][5] + ', '
                        passed = 1
                    #TODO: Display error to user
                    except Exception:
                        #Cannot copy file
                        print "Exception error: %s" % Exception
                        pass
                else:
                    if tkMessageBox.askyesno("Overwrite", "File " + settings[index][5] + " already exists, overwrite?"):
                        try:
                            os.remove(dirname + '/' + settings[index][4] + settings[index][5])
                            shutil.copy(os.getcwd() + '/scripts/' + settings[index][5], dirname + '/' + settings[index][4])
                            string = string + settings[index][2] + ', '
                            string = string + settings[index][5] + ', '
                            checkbox[i].config(foreground = 'blue')
                            passed = 1
                        #TODO: Display Error to user
                        except Exception:
                            #Cannot copy file
                            pass
    if len(string) > 7:
        #Trimming trailing ', '
        string = string[:-2]
        dialMsg("Added Sounds", string, 0)
    

def removeFiles():
    global active, dirSet, settings, dirname, checkbox
    if dirSet == 0:
        dialMsg("No directory set", "Please select your steam directory", 0)
        return
    string = "Removed: "
    i = -1
    for index in active:
        passed = 0
        i+= 1
        if active[index] != -1:
            #If the file exists
            if os.path.isfile(dirname + '/' + settings[index][1] + settings[index][2]):
                try:
                    os.remove(dirname + '/' + settings[index][1] + settings[index][2])
                    if not settings[index][4] != '':
                        string = string + settings[index][2] + ', '
                        checkbox[i].config(foreground = 'red')
                    passed = 1
                #TODO: Display error to user
                except Exception:
                    pass
        if passed and settings[index][4] != '':
            #If the file exists
            if os.path.isfile(dirname + '/' + settings[index][4] + settings[index][5]):
                try:
                    os.remove(dirname + '/' + settings[index][4] + settings[index][5])
                    string = string + settings[index][2] + ', '
                    string = string + settings[index][5] + ', '
                    checkbox[i].config(foreground = 'red')
                #TODO: Display error to user
                except Exception:
                    pass
    if len(string) > 9:
        #Trimming trailing ', '
        string = string[:-2]
        dialMsg("Removed Sounds", string, 0)
    

top = Tkinter.Tk()
top.title("Dota 2 File Installer")
readFiles()
#Default window size
w = 393
h = 165
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
exit = Tkinter.Button(top, width=55, height="2", text="Exit", command = lambda: top.destroy()).grid(row = 1, columnspan=2, column = 0)
lab = Tkinter.Label(top, width=55, height="2", text="Custom Sounds:").grid(row = 2, columnspan=2, column = 0)
vol = Scale(
    top,
    label = "Volume:",
    showvalue = 0,
    length = 350,
    from_ = 0,
    to = 1,
    orient = HORIZONTAL,
    resolution = .05,
    command = change_vol,
)
vol.set(.5)
vol.config(state = "disabled")
i = 0
for name in settings:
    #active[i] = IntVar()
    #active[i].set(-1)
    active[i] = -1
    checkbox[i] = Tkinter.Checkbutton(top, width=24, foreground=checkbox[i], height=2, text=name[0], state="disabled", onvalue=i, offvalue=-1, command =lambda i=i:playSound(i))
    checkbox[i].grid(row = (3 + i/2), column = i%2)
    i+= 1
vol.grid(row= 4 + i/2, columnspan=2, column = 0)
add = Tkinter.Button(top, width=27, height="2", text="Add", state="disabled", command = lambda: addFiles())
add.grid(row= 5 + i/2, columnspan=1, column = 0)
rem = Tkinter.Button(top, width=27, height="2", text="Remove", state="disabled", command = lambda: removeFiles())
rem.grid(row = 5 + i/2, columnspan=1, column = 1)
top.mainloop()
raw_input()


