import sqlite3
import datetime

class database:
    def __init__(self):
        sqlite3.connect('udp.db')
        self.conn = sqlite3.connect('udp.db')
        self.c = self.conn.cursor()

        self.c.execute('''CREATE TABLE IF NOT EXISTS users 
        ([generated_id] INTEGER PRIMARY KEY,
        [user] text,
        [password] text,
        [last_active] datetime,
        UNIQUE(user))''')

        self.c.execute('''CREATE TABLE IF NOT EXISTS messages 
        ([generated_id] INTEGER PRIMARY KEY,
        [user] text,
        [time] datetime,
        [message] text)''')

        self.c.execute('''CREATE TABLE IF NOT EXISTS subscriptions 
        ([user] text,
        [subbed] text)''')

        self.conn.commit()
    
    def insertUser(self, user, hashedPass, time):
        databaseSize = self.c.execute('''SELECT COUNT(*) FROM users''').fetchall()[0][0]

        sql = '''INSERT or ignore INTO users (generated_id, user, password, last_active) VALUES (?, ?, ?, ?)'''
        data = (databaseSize, user, hashedPass, time)
        self.c.execute(sql, data)
        self.conn.commit()

    def authenticateUser(self, user, hashedPass):
        data = (user,)
        userInfo = self.c.execute('''SELECT password FROM users where user = ?''', data).fetchone()
        
        returnValue = False
        if userInfo is not None and userInfo[0] == hashedPass:
            returnValue =  True
        
        return returnValue
    
    def verifyUserExists(self, user):
        data = (user,)
        userInfo = self.c.execute('''SELECT user FROM users where user = ?''', data).fetchone()

        returnValue = False
        if userInfo is not None:
            returnValue = True
        
        return returnValue
    
    def addSub(self, user, subbedTo):
        returnValue = False

        if self.verifyUserExists(subbedTo):

            sql = '''INSERT INTO subscriptions (user, subbed) VALUES (?, ?)'''
            data = (user, subbedTo)
            self.c.execute(sql, data)
            self.conn.commit()

            returnValue = True
        
        return returnValue
    
    def removeSub(self, user, subbedTo):
        returnValue = False
        data = (user, subbedTo)
        userInfo = self.c.execute('''SELECT user FROM subscriptions WHERE user = ? AND subbed = ?''', data).fetchone()

        if userInfo is not None:

            sql = '''DELETE FROM subscriptions WHERE user = ? AND subbed = ?'''
            data = (user, subbedTo)
            self.c.execute(sql, data)
            self.conn.commit()

            returnValue = True
        
        return returnValue

    
    def getSubs(self, user):
        data = (user,)
        userInfo = self.c.execute('''SELECT user FROM subscriptions where subbed = ?''', data).fetchone()
        
        return userInfo
    
    def insertMessage(self, user, time, message):
        databaseSize = self.c.execute('''SELECT COUNT(*) FROM messages''').fetchall()[0][0]

        sql = '''INSERT INTO messages (generated_id, user, time, message) VALUES (?, ?, ?, ?)'''
        data = (databaseSize, user, time, message)
        self.c.execute(sql, data)
        self.conn.commit()
    
    def getMessages(self):
        messageList = self.c.execute('''SELECT * FROM messages''').fetchall()
        return messageList