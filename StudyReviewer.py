
from PIL import Image, ImageGrab

from tkinter import ttk, Text, Entry, Scrollbar, VERTICAL, HORIZONTAL, RIGHT,Y
import tkinter as tk

import sqlite3

import base64

DATABASE = 'StudyHelper.db'

# q represents quesiton
# a represents answer

qPic = None
aPic = None


def init_db():
    #create database and tables
    
    sqliteDB = sqlite3.connect(DATABASE)
    print ("Opened database successfully")

    #sqliteDB.execute('DROP TABLE IF exists student')
    sqliteDB.execute('CREATE TABLE IF NOT EXISTS item (id INTEGER PRIMARY KEY AUTOINCREMENT, qPic LONGBOLB, aPic LONGBOLB, createTime timestamp, lastShowTime timestamp)')

    print ("Tables created successfully")


def focusOnQEntry():
    im = ImageGrab.grabclipboard()
    im.save('qPic.png', 'png')
    global qPicLabel , qPic #有生命周期的问题，必须使用全局变量
    qPic = tk.PhotoImage(file="qPic.png")
    qPicLabel.config(image=qPic)

def focusOnAEntry():
    im = ImageGrab.grabclipboard()
    im.save('aPic.png', 'png')
    global aPicLabel , aPic #有生命周期的问题，必须使用全局变量
    aPic = tk.PhotoImage(file="aPic.png")
    aPicLabel.config(image=aPic)
    aPicLabel.pack()


def addImage():
    saveCurrentImageToDB("qPic.png", "aPic.png")


# def addImageFromAddress():
#     global qPicLabel , qPic #有生命周期的问题，必须使用全局变量
#     qText = qEntry.get()
#     qPic = tk.PhotoImage(file=qText)
#     print(qText)
#     qPicLabel.config(image=qPic)

#     global aPicLabel , aPic #有生命周期的问题，必须使用全局变量
#     aText = aEntry.get()
#     aPic = tk.PhotoImage(file=aText)
#     print(aText)
#     aPicLabel.config(image=aPic)
#     saveImageToDB(qText, aText)


# def saveImageToDB(qPicAddress, aPicAddress):
#     with open(qPicAddress, "rb") as f1:
#         with open(aPicAddress, "rb") as f2:
#             qRes = base64.b64encode(f1.read())
#             aRes = base64.b64encode(f2.read())

#             conn = sqlite3.connect(DATABASE)
#             c = conn.cursor()
#             c.execute("INSERT INTO item(qPic, aPic, createTime, lastShowTime) VALUES(?,?,datetime(),datetime())", (qRes, aRes))
#             conn.commit()
#             c.close()
#             conn.close()

def saveCurrentImageToDB(qPicAddress, aPicAddress):
    with open(qPicAddress, "rb") as f1:
        with open(aPicAddress, "rb") as f2:
            qRes = base64.b64encode(f1.read())
            aRes = base64.b64encode(f2.read())

            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            c.execute("INSERT INTO item(qPic, aPic, createTime, lastShowTime) VALUES(?,?,datetime(),datetime())", (qRes, aRes))
            conn.commit()
            c.close()
            conn.close()


def readImageFromDB():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM item order by lastShowTime ASC")

    item = c.fetchone()
    id = item[0]
    c.execute("UPDATE item SET lastShowTime=datetime() WHERE id=?", (id,))
    conn.commit()
    c.close()
    conn.close()
    if item == None:
        return
    data1 = base64.b64decode(item[1])
    data2 = base64.b64decode(item[2])
    with open("qPic.png", "wb") as f1:
        f1.write(data1)
    with open("aPic.png", "wb") as f2:
        f2.write(data2)

    global qPicLabel , qPic #有生命周期的问题，必须使用全局变量
    qPic = tk.PhotoImage(file="qPic.png")
    qPicLabel.config(image=qPic)

    global aPicLabel , aPic #有生命周期的问题，必须使用全局变量
    aPic = tk.PhotoImage(file="aPic.png")
    aPicLabel.config(image=aPic)
    aPicLabel.pack_forget()

def showAnswer():
    aPicLabel.pack()



init_db()
root = tk.Tk()

#address
qEntry = Entry(root, text="1", validate="focusin",
                validatecommand=focusOnQEntry)

aEntry = Entry(root, text="2", validate="focusin",
                validatecommand=focusOnAEntry)

qPicLabel = tk.Label(root)

aPicLabel = tk.Label(root)

addBtn = tk.Button(root, text='Add', command  = addImage)
nextBtn = tk.Button(root, text='Next', command  = readImageFromDB)
showBtn = tk.Button(root, text='ShowAnswer', command  = showAnswer)
# layout
addBtn.pack()
nextBtn.pack()
showBtn.pack()
qEntry.pack()
qPicLabel.pack()
aEntry.pack()
aPicLabel.pack()


# S1=Scrollbar(root,orient=HORIZONTAL)
# S1.set(0.6,0)
# S1.pack()
# sl = Scrollbar(root)
# sl.pack(side = RIGHT,fill = Y)
readImageFromDB()
root.mainloop()