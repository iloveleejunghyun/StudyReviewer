
from PIL import Image, ImageGrab

from tkinter import ttk, Text, Entry, Scrollbar, VERTICAL, \
HORIZONTAL, RIGHT,Y, messagebox, YES, NO, X, Y
import tkinter as tk

from db import *


# q represents quesiton
# a represents answer

qPic = None
aPic = None
firstClick = True

def showNextItem():
    if readNextItemFromDB():
        global qPicLabel , qPic #有生命周期的问题，必须使用全局变量
        qPic = tk.PhotoImage(file="qPic.png")
        qPicLabel.config(image=qPic)

        global aPicLabel , aPic #有生命周期的问题，必须使用全局变量
        aPic = tk.PhotoImage(file="aPic.png")
        aPicLabel.config(image=aPic)
        aPicLabel.pack_forget()
    else:
        messagebox.showinfo("warn", "Nothing need to review today")

def focusOnQEntry(self):
    im = ImageGrab.grabclipboard()
    if im == None:
        return
    im.save('qPic.png', 'png')
    global qPicLabel , qPic, addBtn #有生命周期的问题，必须使用全局变量
    qPic = tk.PhotoImage(file="qPic.png")
    qPicLabel.config(image=qPic)
    addBtn.focus_set()
    print("question focus")

def focusOnAEntry(self):
    im = ImageGrab.grabclipboard()
    if im == None:
        return
    im.save('aPic.png', 'png')
    global aPicLabel , aPic #有生命周期的问题，必须使用全局变量
    aPic = tk.PhotoImage(file="aPic.png")
    aPicLabel.config(image=aPic)
    aPicLabel.pack()
    addBtn.focus_set()
    print("answer focus")

def addItem():
    res = saveCurrentItemToDB("qPic.png", "aPic.png")
    if res == None:
        controlLable.config(text="Add item success!");
    else:
        controlLable.config(text=res);

def checkFirstClick():
    global firstClick
    if firstClick:
        firstClick = False
        showAnswer()
        return True
    firstClick = True
    return False

def clickNextV():
    if checkFirstClick():
        return
    updateCurrentItemShowTime()
    showNextItem()

def clickNextX():
    if checkFirstClick():
        return
    updateCurrentItemShowTime()
    updateCurrentItemFailTime()
    showNextItem()

def showAnswer():
    aPicLabel.pack()

def deleteCurrentItem():
     #msg box, really to delete?
    if not messagebox.askokcancel("Warning", "Really to delete current images?"):
        return

    res = deleteCurrentItemFromDB()
    if not res:
        messagebox.showerror("error", res)

#============================================================================
# main
#============================================================================
init_db()
root = tk.Tk()
root.title("StudyReviewer")
panelFrame = tk.Frame(root)
countFrame = tk.Frame(panelFrame)
controlFrame = tk.Frame(panelFrame)
nextFrame = tk.Frame(panelFrame)

#count labels
lastReviewTimeLabel = tk.Label(countFrame, text="Last review time:");
passedFailedTimesLabel = tk.Label(countFrame, text="Passed/Failed:");
todayTotalReviewCountLabel = tk.Label(countFrame, text="Today reviewed/ totally:");

#address
# qEntry = Entry(root, text="1", validate="focusin",
#                 validatecommand=focusOnQEntry)
qEntry = Entry(root, text="1")
qEntry.bind("<FocusIn>", focusOnQEntry)

# aEntry = Entry(root, text="2", validate="focusin",
#                 validatecommand=focusOnAEntry)
aEntry = Entry(root, text="2")
aEntry.bind("<FocusIn>", focusOnAEntry)

qPicLabel = tk.Label(root)

aPicLabel = tk.Label(root)

addBtn = tk.Button(controlFrame, text='Add', command  = addItem)
deleteBtn = tk.Button(controlFrame, text='Delete', command  = deleteCurrentItem)
controlLable = tk.Label(controlFrame);

showBtn = tk.Button(nextFrame, text='ShowAnswer', command  = showAnswer)
nextVBtn = tk.Button(nextFrame, text='Next-V', command  = clickNextV)
nextXBtn = tk.Button(nextFrame, text='Next-X', command  = clickNextX)

# layout
panelFrame.pack(expand='yes', fill='x')
countFrame.pack(side='right')
controlFrame.pack(expand='yes', fill='x')
nextFrame.pack(expand='yes', fill='x')

lastReviewTimeLabel.pack();
passedFailedTimesLabel.pack();
todayTotalReviewCountLabel.pack();

addBtn.pack(side='left')
deleteBtn.pack(side='left')
controlLable.pack(side='left')

# showBtn.pack(side='left')
nextVBtn.pack(side='left')
nextXBtn.pack(side='left')

qEntry.pack(expand=YES,fill=X)
qPicLabel.pack()
aEntry.pack(expand=YES,fill=X)
aPicLabel.pack()


# S1=Scrollbar(root,orient=HORIZONTAL)
# S1.set(0.6,0)
# S1.pack()
# sl = Scrollbar(root)
# sl.pack(side = RIGHT,fill = Y)
   

showNextItem()
root.mainloop()