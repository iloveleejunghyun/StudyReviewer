import sqlite3

import base64



DATABASE = 'StudyReviewer.db'
# DATABASE_BACKUP = 'F:\\backupdb\\backup.db'
DATABASE_BACKUP = 'backup.db'

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
 
    #backup db
    backupDB(DATABASE, DATABASE_BACKUP)

    # c.execute("UPDATE item SET lastShowTime= DATETIME('now', 'localtime','-1 day')")
    # conn.commit()
    # c.execute("SELECT lastFailTime, lastShowTime FROM item WHERE DATE(lastFailTime) == DATE('now', 'localtime', '-1 day')")
    # c.execute("SELECT DATEtime('now', 'localtime','-1 day')")

    # item = c.fetchall()
    # if item != None:
    #     print(list(item))
    #     print(len(item))
    c.close()
    conn.close()
    print ("Tables created successfully")
    return True

def backupDB(dbName, backFileName):
    with open(dbName, 'rb') as read:
        with open(backFileName,'wb') as f:
            for line in read.readlines():
                f.write(line)

def countFromDB(createdToday = True):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    if createdToday == True:
        c.execute("SELECT COUNT(*) FROM item WHERE DATE(createTime) = DATE('now','localtime')")
        count = c.fetchone()[0]
    c.close()
    conn.close()
    return count

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


def insertItemToDB(id, qPic, aPic, createTime, lastShowTime, lastFailTime, passTimes, failTimes):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO item(id, qPic, aPic, createTime, lastShowTime, lastFailTime, passTimes, failTimes) VALUES(?,?,?,?,?,?,?,?)"
           , (id, qPic, aPic, createTime, lastShowTime, lastFailTime, passTimes, failTimes))
    conn.commit()
    print(c.fetchone())
    c.close()
    conn.close()
    return True

def updateCurrentItem(itemId = None, lastShowTime = None, passTimes = None, failTimes = None):
    #update current item last_show_time
    if itemId == None:
        global currentItemId
        itemId = currentItemId
    if itemId != None:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        if lastShowTime == True:
            c.execute("UPDATE item SET lastShowTime=datetime('now', 'localtime') WHERE id=?", (itemId,))
        if passTimes == '+1':
             c.execute("UPDATE item SET passTimes=passTimes+1 WHERE id=?", (itemId,))
        if failTimes == '+1':
            c.execute("UPDATE item SET failTimes=failTimes+1 WHERE id=?", (itemId,))
        conn.commit()
        c.close()
        conn.close()

def readNextItemFromDB(itemId = None):

    global currentItemId
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    if itemId != None:
        c.execute("SELECT id, qPic, aPic, passTimes, failTimes, lastFailTime, lastShowTime FROM item WHERE id=(?)", (itemId,))
    else:
        c.execute("SELECT id, qPic, aPic, passTimes, failTimes, lastFailTime, lastShowTime e FROM item WHERE DATE(lastShowTime) != DATE('now', 'localtime') and DATE(lastFailTime) in (DATE('now', 'localtime', '-1 day'), DATE('now', 'localtime', '-2 day'), DATE('now', 'localtime', '-4 day'), DATE('now', 'localtime', '-7 day'), DATE('now', 'localtime', '-14 day') ) order by lastFailTime ASC")

    item = c.fetchone()
    if item == None:
        #no data in current database
        print("no data in database to show")
        return False, 0, 0, 0, 0
    print(item[0])
    currentItemId = item[0]
    # c.execute("UPDATE item SET lastShowTime = datetime('now', 'localtime') WHERE id=?", (currentItemId,))
    # conn.commit()
    c.close()
    conn.close()

    if item[1] != None:
        data1 =  base64.b64decode(item[1])
        with open("qPic.png", "wb") as f1:
            f1.write(data1)
            
    if item[2] != None:
        data2 = base64.b64decode(item[2])
        with open("aPic.png", "wb") as f2:
            f2.write(data2)

    passTimes = item[3]
    failTimes = item[4]
    lastFailTime = item[5]
    lastShowTime = item[6]
    return True, passTimes, failTimes, lastFailTime, lastShowTime


def deleteCurrentItemFromDB():
    global currentItemId
    if not currentItemId:
        #msg box no id
        return "Error","Can't find current item. No Picture!"

    deleteItemFromDB(currentItemId)
    currentItemId = None
    readNextItemFromDB()
    return None

def deleteItemFromDB(itemId):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("DELETE FROM item WHERE id = ?", (itemId,))
    conn.commit()
    c.close()
    conn.close()
    return None

def getReviewItemCountToday():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM item WHERE DATE(lastShowTime) != DATE('now', 'localtime') and DATE(lastFailTime) in (DATE('now', 'localtime', '-1 day'), DATE('now', 'localtime', '-2 day'), DATE('now', 'localtime', '-4 day'), DATE('now', 'localtime', '-7 day'), DATE('now', 'localtime', '-14 day') ) order by lastFailTime ASC")
    toReviewCount = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM item WHERE DATE(lastShowTime) == DATE('now', 'localtime') and DATE(lastFailTime) in (DATE('now', 'localtime', '-1 day'), DATE('now', 'localtime', '-2 day'), DATE('now', 'localtime', '-4 day'), DATE('now', 'localtime', '-7 day'), DATE('now', 'localtime', '-14 day') ) order by lastFailTime ASC")
    reviewedSuccessCount = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM item WHERE DATE(lastShowTime) == DATE('now', 'localtime') and DATE(lastFailTime) == DATE('now', 'localtime') and DATE(createTime) != DATE('now', 'localtime')")
    reviewedFailTodayCount = c.fetchone()[0]
    return (reviewedSuccessCount+reviewedFailTodayCount, reviewedSuccessCount+reviewedFailTodayCount+toReviewCount)

def init_deleteItem():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS deleteItem AS SELECT * FROM item WHERE 1=2")
    conn.commit()
    c.close()
    conn.close() 
    pass

def moveItemToDeleteItem(itemId):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO deleteItem SELECT * FROM item WHERE id=(?)", (itemId,))
    c.execute("DELETE FROM item WHERE id=(?)", (itemId,))
    conn.commit()
    c.close()
    conn.close()
    pass

def readDeleteItem(itemId):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT id, qPic, aPic, passTimes, failTimes, lastFailTime, lastShowTime FROM deleteItem WHERE id=(?)", (itemId,))
    item = c.fetchone()
    if item == None:
        #no data in current database
        print("no data in database to show")
        return False, 0, 0, 0, 0
    c.close()
    conn.close()

    passTimes = item[3]
    failTimes = item[4]
    lastFailTime = item[5]
    lastShowTime = item[6]
    return True, passTimes, failTimes, lastFailTime, lastShowTime
    pass

def deleteDeleteItem(itemId):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("DELETE FROM deleteItem WHERE id=(?)", (itemId,))
    conn.commit()
    c.close()
    conn.close()
    pass