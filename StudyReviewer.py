
from PIL import Image, ImageGrab
from threading import Timer
from tkinter import ttk, Text, Entry, Scrollbar, VERTICAL, \
HORIZONTAL, RIGHT,Y, messagebox, YES, NO, X, Y, Canvas, LEFT, BOTH, NW
import tkinter as tk

from db import *
from scrolltest import QAFrame

# q represents quesiton
# a represents answer

qPic = None
aPic = None
firstClick = True
infoTimer = None

def showInfoTimer(info):
    controlLable.config(text=info)
    global infoTimer
    if infoTimer:
        infoTimer.cancel()
    infoTimer = Timer(5.0, cleanInfo)
    infoTimer.start()

def cleanInfo():
    global controlLable
    controlLable.config(text="")
    global infoTimer
    infoTimer = None

def showNextItem():
    res, passTimes, failTimes, lastFailTime, lastShowTime = readNextItemFromDB()
    if res:
        # global qPicLabel , qPic #有生命周期的问题，必须使用全局变量
        global qPic, aPic
        qPic = tk.PhotoImage(file="qPic.png")

        # global aPicLabel , aPic #有生命周期的问题，必须使用全局变量
        aPic = tk.PhotoImage(file="aPic.png")
        qaFrame.updateQLabel(qPic)
        qaFrame.updateALabel(aPic)
        qaFrame.hideALabel()

        lastReviewTimeLabel.configure(text=f"Last failed time:{lastFailTime}")
        passedFailedTimesLabel.configure(text=f"Passed/Failed:{passTimes}/{failTimes}")
    else:
        messagebox.showinfo("warn", "Nothing need to review today")
    reviewedCount, totalCount = getReviewItemCountToday()
    todayTotalReviewCountLabel.config(text=f"Today reviewed :{reviewedCount}/{totalCount}")

def focusOnQEntry(self):
    im = ImageGrab.grabclipboard()
    if im == None:
        return
    im.save('qPic.png', 'png')
    # global qPicLabel , qPic, addBtn #有生命周期的问题，必须使用全局变量
    # qPic = tk.PhotoImage(file="qPic.png")
    # qPicLabel.config(image=qPic)
    global qPic, addBtn #有生命周期的问题，必须使用全局变量
    qPic = tk.PhotoImage(file="qPic.png")
    qaFrame.updateQLabel(qPic)
    addBtn.focus_set()
    print("question focus")

def focusOnAEntry(self):
    im = ImageGrab.grabclipboard()
    if im == None:
        return
    im.save('aPic.png', 'png')
    # global aPicLabel , aPic #有生命周期的问题，必须使用全局变量
    # aPic = tk.PhotoImage(file="aPic.png")
    # aPicLabel.config(image=aPic)
    # aPicLabel.pack()
    global aPic #有生命周期的问题，必须使用全局变量
    aPic = tk.PhotoImage(file="aPic.png")
    qaFrame.updateALabel(aPic)
    qaFrame.showALabel()

    addBtn.focus_set()
    print("answer focus")

def addItem():
    res = saveCurrentItemToDB("qPic.png", "aPic.png")
    if res == None:
        showInfoTimer("Add item success!")
        # controlLable.config(text="Add item success!");
    else:
        showInfoTimer(res)
        # controlLable.config(text=res);

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
    updateCurrentItem(lastShowTime=True, passTimes='+1')
    showNextItem()

def clickNextX():
    if checkFirstClick():
        return
    updateCurrentItem(lastShowTime=True, failTimes='+1')
    showNextItem()

def showAnswer():
    # aPicLabel.pack()
    qaFrame.showALabel()

def deleteCurrentItem():
     #msg box, really to delete?
    if not messagebox.askokcancel("Warning", "Really to delete current images?"):
        return

    res = deleteCurrentItemFromDB()
    if res:
        messagebox.showerror("error", res)
    showNextItem()

def processKeyboardEvent(ke):
    if(ke.keysym == "Left"):
        clickNextX()
    elif(ke.keysym == "Right"):
        clickNextV()
        
    print("ke.keysym", ke.keysym)  # 按键别名
    print("ke.char", ke.char)  # 按键对应的字符
    print("ke.keycode", ke.keycode)  # 按键的唯一代码，用于判断按下的是哪个键</class></key></button-1>
#============================================================================
# main
#============================================================================
init_db()
root = tk.Tk()
root.title("StudyReviewer")
root.bind(sequence="<Key>", func=processKeyboardEvent)
panelFrame = tk.Frame(root)
countFrame = tk.Frame(panelFrame)
controlFrame = tk.Frame(panelFrame)
nextFrame = tk.Frame(panelFrame)
qaFrame = QAFrame(root, focusOnQEntry, focusOnAEntry)
#count labels
lastReviewTimeLabel = tk.Label(countFrame, text="Last failed time:");
passedFailedTimesLabel = tk.Label(countFrame, text="Passed/Failed:");
todayTotalReviewCountLabel = tk.Label(countFrame, text="Today reviewed :");

#address
# qEntry = Entry(root, text="1")
# qEntry.bind("<FocusIn>", focusOnQEntry)

# aEntry = Entry(root, text="2")
# aEntry.bind("<FocusIn>", focusOnAEntry)

# qPicLabel = tk.Label(root)
# aPicLabel = tk.Label(root)

addBtn = tk.Button(controlFrame, text='Add', command  = addItem)
deleteBtn = tk.Button(controlFrame, text='Delete', command  = deleteCurrentItem)
controlLable = tk.Label(controlFrame);


showBtn = tk.Button(nextFrame, text='ShowAnswer', command  = showAnswer)
nextXBtn = tk.Button(nextFrame, text='Next-X', command  = clickNextX)
nextVBtn = tk.Button(nextFrame, text='Next-V', command  = clickNextV)


# layout
panelFrame.pack(side='top', expand='yes', fill='x')
countFrame.pack(side='right')
controlFrame.pack(expand='yes', fill='x')
nextFrame.pack(expand='yes', fill='x')

lastReviewTimeLabel.pack();
passedFailedTimesLabel.pack();
todayTotalReviewCountLabel.pack();

addBtn.pack(side='left')
deleteBtn.pack(side='left')
controlLable.pack(side='left')

nextXBtn.pack(side='left')
nextVBtn.pack(side='left')



qaFrame.pack()
# qEntry.pack(expand=YES,fill=X)
# qPicLabel.pack()
# aEntry.pack(expand=YES,fill=X)
# aPicLabel.pack()


# S1=Scrollbar(root,orient=HORIZONTAL)
# S1.set(0.6,0)
# S1.pack()
# sl = Scrollbar(root)
# sl.pack(side = RIGHT,fill = Y)
   

showNextItem()
root.focus_force() # 必须使用， 否则不能获取焦点。 进而不能使用按键快捷键。
root.mainloop()