
from PIL import Image, ImageGrab
from threading import Timer
from tkinter import ttk, Text, Entry, Scrollbar, VERTICAL, \
HORIZONTAL, RIGHT,Y, messagebox, YES, NO, X, Y, Canvas, LEFT, BOTH, NW
import tkinter as tk

import db
from qawindow import QAFrame
from hotkey import Hotkey
import sound

# q represents quesiton
# a represents answer
class StudyReviewerWindow(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        master.resizable(0, 0)
        self.master = master
        self.qPic = None
        self.aPic = None
        self.firstClick = True
        self.infoTimer = None

        db.init_db()
        self.master.title("StudyReviewer")
        self.master.bind(sequence="<Key>", func=self.processKeyboardEvent)
        self.pack()

        self.panelFrame = tk.Frame(self)
        self.countFrame = tk.Frame(self.panelFrame)
        self.controlFrame = tk.Frame(self.panelFrame)
        self.nextFrame = tk.Frame(self.panelFrame)
        self.qaFrame = QAFrame(self, self.focusOnQEntry, self.focusOnAEntry)
        #count labels
        self.lastReviewTimeLabel = tk.Label(self.countFrame, text="Last failed time:")
        self.passedFailedTimesLabel = tk.Label(self.countFrame, text="Passed/Failed:")
        self.todayTotalReviewCountLabel = tk.Label(self.countFrame, text="Today reviewed :")
        self.todayAddedCountLabel = tk.Label(self.countFrame, text="Today Added :")

        self.addBtn = tk.Button(self.controlFrame, text='Add(F4)', command  = self.addItem)
        self.deleteBtn = tk.Button(self.controlFrame, text='Delete', command  = self.deleteCurrentItem)
        self.controlLable = tk.Label(self.controlFrame);
        self.classList = tk.Listbox(self.controlFrame);
        categoryList = db.getCategoryList()
        self.classDic = dict()
        self.categoryIdToIndex = dict()

        i = 0
        for row in categoryList:
            self.classList.insert(row[0], row[1])
            self.classDic[row[1]] = row[0] # key=name, value=id
            self.categoryIdToIndex[row[0]] = i # key=category_id, value=index in listBox
            i += 1
            # print(row)

        self.showBtn = tk.Button(self.nextFrame, text='ShowAnswer', command  = self.showAnswer)
        self.nextXBtn = tk.Button(self.nextFrame, text='Next-X', command  = self.clickNextX)
        self.nextVBtn = tk.Button(self.nextFrame, text='Next-V', command  = self.clickNextV)


        # layout
        self.panelFrame.pack(side='top', expand='yes', fill='x')
        self.countFrame.pack(side='right')
        self.controlFrame.pack(expand='yes', fill='x')
        self.nextFrame.pack(expand='yes', fill='x')

        self.lastReviewTimeLabel.pack()
        self.passedFailedTimesLabel.pack()
        self.todayTotalReviewCountLabel.pack()
        self.todayAddedCountLabel.pack()

        self.addBtn.pack(side='left')
        self.deleteBtn.pack(side='left')
        self.controlLable.pack(side='left')
        self.classList.pack(side='left', anchor='w')
        self.classList.config(height = len(categoryList))

        self.nextXBtn.pack(side='left')
        self.nextVBtn.pack(side='left')

        self.qaFrame.pack()


        # add hot key function
        self.hot = Hotkey(self.focusOnQEntry, self.focusOnAEntry, self.addItem)
        self.hot.listenDaemon()

        self.showNextItem()
        self.focus_force() # 必须使用， 否则不能获取焦点。 进而不能使用按键快捷键。

    def showInfoTimer(self, info):
        self.controlLable.config(text=info)
        if self.infoTimer:
            self.infoTimer.cancel()
        self.infoTimer = Timer(5.0, self.cleanInfo)
        self.infoTimer.start()

    def cleanInfo(self):
        self.controlLable.config(text="")
        self.infoTimer = None

    def showNextItem(self):
        self.firstClick = True # update click count
        res, passTimes, failTimes, lastFailTime, lastShowTime, category_id = db.readNextItemFromDB()
        if res:
            print(f"read category_id={category_id}")
            # global qPicLabel , qPic #有生命周期的问题，必须使用全局变量
            self.qPic = tk.PhotoImage(file="qPic.png")

            # global aPicLabel , aPic #有生命周期的问题，必须使用全局变量
            self.aPic = tk.PhotoImage(file="aPic.png")
            self.qaFrame.updateQLabel(self.qPic)
            self.qaFrame.updateALabel(self.aPic)
            self.qaFrame.hideALabel()

            self.lastReviewTimeLabel.configure(text=f"Last failed time:{lastFailTime}")
            self.passedFailedTimesLabel.configure(text=f"Passed/Failed:{passTimes}/{failTimes}")
            # self.classList.selection_set(0,0)
            self.classList.selection_clear(0, tk.END)
            index = self.categoryIdToIndex[category_id]
            self.classList.selection_set(index)
            self.classList.see(index)
            self.classList.activate(index)
            self.classList.selection_anchor(index)
            # self.classList.select_anchor(self.categoryIdToIndex[category_id])
        else:
            messagebox.showinfo("warn", "Nothing need to review today")
        reviewedCount, totalCount = db.getReviewItemCountToday()
        self.todayTotalReviewCountLabel.config(text=f"Today reviewed :{reviewedCount}/{totalCount}")
        addedCount = db.countFromDB(createdToday=True)
        self.todayAddedCountLabel.config(text=f"Today Added: {addedCount}")

    def focusOnQEntry(self, event=None):
        im = ImageGrab.grabclipboard()
        if im == None:
            return
        im.save('qPic.png', 'png')
        # global qPicLabel , qPic, addBtn #有生命周期的问题，必须使用全局变量
        # qPic = tk.PhotoImage(file="qPic.png")
        # qPicLabel.config(image=qPic)
        # global qPic, addBtn #有生命周期的问题，必须使用全局变量
        self.qPic = tk.PhotoImage(file="qPic.png")
        self.qaFrame.updateQLabel(self.qPic)
        self.addBtn.focus_set()
        print("question focus")
        sound.ding()

    def focusOnAEntry(self, event=None):
        im = ImageGrab.grabclipboard()
        if im == None:
            return
        im.save('aPic.png', 'png')
        # global aPicLabel , aPic #有生命周期的问题，必须使用全局变量
        # aPic = tk.PhotoImage(file="aPic.png")
        # aPicLabel.config(image=aPic)
        # aPicLabel.pack()
        # global aPic #有生命周期的问题，必须使用全局变量
        self.aPic = tk.PhotoImage(file="aPic.png")
        self.qaFrame.updateALabel(self.aPic)
        self.qaFrame.showALabel()

        self.addBtn.focus_set()
        print("answer focus")
        sound.ding()

    def addItem(self):
        selected = self.classList.get(tk.ANCHOR)
        category_id = self.classDic[selected]
        print(f"select {selected}, {category_id}")
        res = db.saveCurrentItemToDB("qPic.png", "aPic.png", category_id)
        if res == None:
            addedCount = db.countFromDB(createdToday=True)
            self.todayAddedCountLabel.config(text=f"Today Added: {addedCount}")
            self.showInfoTimer("Add item success!")
            # controlLable.config(text="Add item success!");
        else:
            self.showInfoTimer(res)
            sound.ding()
            # controlLable.config(text=res);

    def checkFirstClick(self):
        # global firstClick
        if self.firstClick:
            self.firstClick = False
            self.showAnswer()
            return True
        self.firstClick = True
        return False

    def clickNextV(self):
        if self.checkFirstClick():
            return
        selected = self.classList.selection_get()
        category_id = self.classDic[selected]
        print(f"select {selected}, {category_id}")
        db.updateCurrentItem(lastShowTime=True, passTimes='+1', category_id=category_id)
        self.showNextItem()

    def clickNextX(self):
        if self.checkFirstClick():
            return
        selected = self.classList.selection_get()
        category_id = self.classDic[selected]
        print(f"select {selected}, {category_id}")
        db.updateCurrentItem(lastShowTime=True, failTimes='+1', category_id=category_id)
        self.showNextItem()

    def showAnswer(self):
        # aPicLabel.pack()
        self.qaFrame.showALabel()

    def deleteCurrentItem(self):
        #msg box, really to delete?
        if not messagebox.askokcancel("Warning", "Really to delete current images?"):
            return

        res = db.deleteCurrentItemFromDB()
        if res:
            messagebox.showerror("error", res)
        self.showNextItem()

    def processKeyboardEvent(self, ke):
        if(ke.keysym == "Left"):
            self.clickNextX()
        elif(ke.keysym == "Right"):
            self.clickNextV()
            
        print("ke.keysym", ke.keysym)  # 按键别名
        # print("ke.char", ke.char)  # 按键对应的字符
        # print("ke.keycode", ke.keycode)  # 按键的唯一代码，用于判断按下的是哪个键</class></key></button-1>
#============================================================================
# main
#============================================================================

if __name__ == "__main__":
    root = tk.Tk()
    window = StudyReviewerWindow(root)
    root.mainloop()