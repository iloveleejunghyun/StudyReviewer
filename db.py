import sqlite3

import base64



DATABASE = 'StudyReviewer.db'

currentItemId =None

def init_db():
    #create database and tables
    
    sqliteDB = sqlite3.connect(DATABASE)
    print ("Opened database successfully")

    #sqliteDB.execute('DROP TABLE IF exists student')
    sqliteDB.execute('CREATE TABLE IF NOT EXISTS item (id INTEGER PRIMARY KEY AUTOINCREMENT, qPic LONGBOLB, aPic LONGBOLB, createTime TIMESTAMP, lastShowTime TIMESTAMP)')
    sqliteDB.close()


    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    #add passTimes
    try:
        c.execute("SELECT passTimes FROM item")
        item = c.fetchone()
    except sqlite3.OperationalError:
        conn.execute('ALTER TABLE item ADD passTimes INT DEFAULT 0')
    
    #add failTimes
    try:
        c.execute("SELECT failTimes FROM item")
        item = c.fetchone()
    except sqlite3.OperationalError:
        conn.execute('ALTER TABLE item ADD failTimes INT DEFAULT 0')

    #add lastFailTime
    try:
        c.execute("SELECT lastFailTime FROM item")
        item = c.fetchone()
    except sqlite3.OperationalError:
        conn.execute('ALTER TABLE item ADD lastFailTime TIMESTAMP')
 
    # c.execute("UPDATE item SET lastShowTime= DATETIME('now', 'localtime','-1 day')")
    # conn.commit()
    c.execute("SELECT lastFailTime, lastShowTime FROM item WHERE DATE(lastFailTime) == DATE('now', 'localtime', '-1 day')")
    # c.execute("SELECT DATEtime('now', 'localtime','-1 day')")

    item = c.fetchall()
    if item != None:
        print(list(item))
        print(len(item))
    c.close()
    conn.close()
    print ("Tables created successfully")




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
#             c.execute("INSERT INTO item(qPic, aPic, createTime, lastShowTime) VALUES(?,?,datetime('now', 'localtime'),datetime('now', 'localtime'))", (qRes, aRes))
#             conn.commit()
#             c.close()
#             conn.close()

def findSameImages(qRes, aRes):
    #todo add code.
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM item WHERE qPic=? and aPic=?", (qRes,aRes))

    item = c.fetchone()
    if item == None:
        #no data in current database
        print("no data in db")
        return False
    print("find data in db")
    return True

def saveCurrentItemToDB(qPicAddress, aPicAddress):
    with open(qPicAddress, "rb") as f1:
        with open(aPicAddress, "rb") as f2:
            qRes = base64.b64encode(f1.read())
            aRes = base64.b64encode(f2.read())
            if findSameImages(qRes, aRes):
                # messagebox.showwarning("Warning", "Already stored same images!");
                return "Already stored same images!";
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            c.execute("INSERT INTO item(qPic, aPic, createTime, lastShowTime, lastFailTime) VALUES(?,?,datetime('now', 'localtime'),datetime('now', 'localtime'), datetime('now', 'localtime'))", (qRes, aRes))
            conn.commit()
            c.close()
            conn.close()
            return None
            # findSameImages(qRes, aRes)
    return "Can't open files{qPicAddress}, {aPicAddress}. Please check!!";


def updateCurrentItemShowTime():
    #update current item last_show_time
    global currentItemId
    if not currentItemId:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("UPDATE item SET lastShowTime=datetime('now', 'localtime') WHERE id=?", (currentItemId,))
        conn.commit()
        c.close()
        conn.close()


def updateCurrentItemFailTime():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    global currentItemId
    c.execute("UPDATE item SET lastFailTime=datetime('now', 'localtime') WHERE id=?", (currentItemId,))
    conn.commit()
    c.close()
    conn.close()

def readNextItemFromDB():

    global currentItemId
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    #c.execute("SELECT * FROM item WHERE DATE(lastShowTime) != DATE('now') and DATE(lastFailTime) in (DATE('now', '-1 day'), DATE('now', '-2 day'), DATE('now', '-4 day'), DATE('now', '-7 day'), DATE('now', '-14 day') ) order by lastFailTime ASC")
    c.execute("SELECT * FROM item WHERE DATE(lastShowTime) != DATE('now', 'localtime') and DATE(lastFailTime) in (DATE('now', 'localtime', '-1 day'), DATE('now', 'localtime', '-2 day'), DATE('now', 'localtime', '-4 day'), DATE('now', 'localtime', '-7 day'), DATE('now', 'localtime', '-14 day') ) order by lastFailTime ASC")

    item = c.fetchone()
    if item == None:
        #no data in current database
        print("no data in database to show")
        return False
    print(item)
    currentItemId = item[0]
    # c.execute("UPDATE item SET lastShowTime = datetime('now', 'localtime') WHERE id=?", (currentItemId,))
    # conn.commit()
    c.close()
    conn.close()

    data1 = base64.b64decode(item[1])
    data2 = base64.b64decode(item[2])
    with open("qPic.png", "wb") as f1:
        f1.write(data1)
    with open("aPic.png", "wb") as f2:
        f2.write(data2)
    return True


def deleteCurrentItemFromDB():
    global currentItemId
    if not currentItemId:
        #msg box no id
        # messagebox.showinfo("Error","Can't find current item. No Picture!")
        return "Error","Can't find current item. No Picture!"

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("DELETE FROM item WHERE id = ?", (currentItemId,))
    conn.commit()
    c.close()
    conn.close()
    currentItemId = None
    readNextItemFromDB()
    return None