import unittest
import db
import os
import sys
import hashlib
import datetime
# from hotkey import Hotkey
import time

class dbtest(unittest.TestCase):
    def setUp(self):
        db.init_db()
        db.init_deleteItem()
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def testConnect(self):
        self.assertTrue(db.init_db())

    def testBackUp(self):
        
        path = os.getcwd()
        print(path)
        path = path + '/' + db.DATABASE
        print(path)
        db.backupDB(path, db.DATABASE_BACKUP)
        originMD5 = 1
        backupMD5 = 2
        with open(path, 'rb') as f1:
            with open(db.DATABASE_BACKUP, 'rb') as f2:
                originMD5 = hashlib.md5(f1.read()).hexdigest()
                backupMD5 = hashlib.md5(f2.read()).hexdigest()
        self.assertEqual(originMD5, backupMD5)

    def testGetTotal(self):
        reviewedCount, total = db.getReviewItemCountToday()
        print(f"reviewedCount={reviewedCount}")
        print(f"total={total}")
        self.assertGreaterEqual(total, reviewedCount)
        
    def testReadNextItemFromDB(self):
        db.deleteItemFromDB(0)
        time = datetime.datetime.now()
        time = time.strftime("%Y-%m-%d %H:%M:%S")
        db.insertItemToDB(0,None, None, time, time, time, 1, 2 );
        res, passTimes, failTimes, lastFailTime, lastShowTime = db.readNextItemFromDB(0)
        print(res, passTimes, failTimes, lastFailTime)
        db.deleteItemFromDB(0)
        self.assertTrue(res)
        self.assertEqual(passTimes, 1)
        self.assertEqual(failTimes, 2)
        self.assertEqual(lastFailTime, time)

    def testUpdateCurrentItem(self):
        db.deleteItemFromDB(0)
        time = '2020-03-25 00:00:47'
        db.insertItemToDB(0,None, None, time, time, time, 1, 2 );
        db.updateCurrentItem(0, True, '+1', '+1')
        
        res, passTimes, failTimes, lastFailTime, lastShowTime = db.readNextItemFromDB(0)
        time = datetime.datetime.now()
        time = time.strftime("%Y-%m-%d %H:%M:%S")
        db.deleteItemFromDB(0)
        self.assertTrue(res)
        self.assertEqual(passTimes, 2)
        self.assertEqual(failTimes, 3)
        self.assertEqual(lastShowTime, time)

    def testCount(self):
        count = db.countFromDB(createdToday = True)
        print(f"Today added {count} items")

    def testDeleteItem(self):
        itemId = 0
        db.deleteItemFromDB(itemId)
        time = '2020-03-25 00:00:47'
        db.insertItemToDB(0,None, None, time, time, time, 1, 2 )
        db.moveItemToDeleteItem(itemId)
        res, passTimes, failTimes, lastFailTime, lastShowTime = db.readNextItemFromDB(itemId)
        self.assertFalse(res)
        res, passTimes, failTimes, lastFailTime, lastShowTime = db.readDeleteItem(itemId)
        self.assertTrue(res)
        res = db.deleteDeleteItem(itemId)
        res, passTimes, failTimes, lastFailTime, lastShowTime = db.readDeleteItem(itemId)
        self.assertFalse(res)
    
    # def testHotkey(self):
    #     def call1():
    #         print("press f1")
    #     def call2():
    #         print("press f2")
    #     hot = Hotkey(call1, call2)
    #     hot.listenDaemon()
    #     time.sleep(5.0)
    #     #https://github.com/moses-palmer/pynput/issues/6

if __name__ == '__main__':
    unittest.main()