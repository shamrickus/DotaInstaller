import Tkinter, os
from tkFileDialog import askdirectory
from Tkinter import Tk, Frame, Button


def getSteamDir():
    dirname = askdirectory()
    if not os.path.exists(dirname):
        print "bad"
    else:
        print "good"

top = Tkinter.Tk()
top.title("Dota 2 Sound Installer")
w = 640
h = 480
sw = top.winfo_screenwidth()
sh = top.winfo_screenheight()
x = (sw - w) / 2
y = (sh - h) / 2
top.geometry("%dx%d+%d+%d" % (w, h, x, y))

start = Tkinter.Button(top, text="Locate Steam Directory", command = getSteamDir)
start.pack()
top.mainloop()
    


