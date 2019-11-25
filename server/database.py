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
        ([generated_id] INTEGER PRIMARY KEY,
        [user] text,
        [subbed] text)''')

        self.conn.commit()
    
    def insertUser(self, user, hashedPass, time):
        databaseSize = self.c.execute('''SELECT COUNT(*) FROM users''').fetchall()[0][0]

        sql = '''INSERT or ignore INTO users (generated_id, user, password, last_active) VALUES (?, ?, ?, ?)'''
        data = (databaseSize, user, hashedPass, time)
        print(data)
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

