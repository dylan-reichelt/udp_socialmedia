import socket
import sys
import random
import datetime
import threading

from user import User
from aes_encryption import aes
from database import database

class Server:
    def __init__(self):
        self.db = database()
        
        self.tokenDict = {}
        self.keyDict = {}

        # Creates a UDP Socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Bind the socket to the port
        self.server_address = ('localhost', 10000)
        self.sock.bind(self.server_address)

    def listen(self):

        print('\nwaiting to receive message')
        data, address = self.sock.recvfrom(4096)
        
        if "|20|0|0|" in data.decode("utf-8"):
            return [data.decode("utf-8"), address]
        else: 
            key = self.keyDict[address]
            data = self.decrypt(data.decode("utf-8"), key)

        return [data, address]
    
    def send(self, data, address):
        key = self.keyDict[address]
        data = self.encrypt(data, key).encode("ascii", "backslashreplace")
        return self.sock.sendto(data, address)
    
    def logon(self, name, password, address):
        
        #logon successful name and password match
        if self.db.authenticateUser(name, password):
            
            token = 0
            while True:
                token = self.createtoken()
                if token not in self.tokenDict.keys():
                    break
            

            tempUser = User()
            tempUser.User = name
            tempUser.Online = True
            tempUser.Token = str(token)
            tempUser.address = address
            tempUser.lastActive = datetime.datetime.now()
            
            self.tokenDict.update({str(token): tempUser})
            sendData = b'D|R|03|' + str(token).encode("ascii", "backslashreplace") + b'|0|0'
            return sendData
        else:
            sendData = b'D|R|04|0|0|0'
            return sendData
        
    def subscribe(self, user, token):

        sendData = b'D|R|0|0|0|0'
        if self.checkLogin(token):
            tempUser = self.tokenDict[token]
            tempUser.lastActive = datetime.datetime.now()
            if self.db.addSub(tempUser.User, user):
                sendData = b'D|R|06|' + str(token).encode("ascii", "backslashreplace") + b'|0|0'
            else:
                sendData = b'D|R|07|' + str(token).encode("ascii", "backslashreplace") + b'|0|0'
        else:
            sendData = b'D|R|01|' + str(token).encode("ascii", "backslashreplace") + b'|0|0'
            
        return sendData
    
    def unsubscribe(self, user, token):

        sendData = b'D|R|0|0|0|0'
        if self.checkLogin(token):
            tempUser = self.tokenDict[token]
            tempUser.lastActive = datetime.datetime.now()
            if self.db.removeSub(tempUser.User, user):
                sendData = b'D|R|09|' + str(token).encode("ascii", "backslashreplace") + b'|0|0'
            else:
                sendData = b'D|R|10|' + str(token).encode("ascii", "backslashreplace") + b'|0|0'
            
        else:
            sendData = b'D|R|01|' + str(token).encode("ascii", "backslashreplace") + b'|0|0'
            
        return sendData
    
    def post(self, payload, token):

        sendData = b'D|R|0|0|0|0'
        
        if self.checkLogin(token):
            userData = self.tokenDict[token]
            userData.lastActive = datetime.datetime.now()
            payloadFinal = "<" + userData.User + ">" + payload
            self.db.insertMessage(userData.User, datetime.datetime.now(), payload)

            subList = self.db.getSubs(userData.User)

            if subList is not None:
                for tempUser in self.tokenDict.values():
                    if tempUser.User in subList:
                        forwardData = b'D|R|13|' + str(tempUser.Token).encode("ascii", "backslashreplace") + b'|0|' + str(payloadFinal).encode("ascii", "backslashreplace")
                        self.send(forwardData, tempUser.address)
                        tempData, tempAddress = self.listen()
            
            sendData = b'D|R|12|' + str(token).encode("ascii", "backslashreplace") + b'|0|0'
        
        else:
            sendData = b'D|R|01|' + str(token).encode("ascii", "backslashreplace") + b'|0|0'
            
        return sendData
    
    def retrieve(self, token, number):
        sendData = b'D|R|0|0|0|0'
        if self.checkLogin(token):
            userData = self.tokenDict[token]
            userData.lastActive = datetime.datetime.now()
            messageList = self.db.getMessages()
            messageList.reverse()
            for listMessage in messageList:
                if number == 0:
                    break
                
                user = listMessage[1]
                message = listMessage[3]
                subList = self.db.getSubs(user)
                finalMessage = "<" + user + ">" + message

                if subList is not None:
                    if userData.User in subList:
                        forwardData = b'D|R|16|' + str(token).encode("ascii", "backslashreplace") + b'|0|' + finalMessage.encode("ascii", "backslashreplace")
                        self.send(forwardData, userData.address)
                        number += -1
            
            sendData = b'D|R|17|' + str(token).encode("ascii", "backslashreplace") + b'|0|0'
        else:
            sendData = b'D|R|01|' + str(token).encode("ascii", "backslashreplace") + b'|0|0'

        return sendData
    
    def logout(self, token):
        sendData = b'D|R|0|0|0|0'
        if self.checkLogin(token):
            del self.tokenDict[token]
            sendData = b'D|R|19|' + str(token).encode("ascii", "backslashreplace") + b'|0|0'
        else:
            sendData = b'D|R|01|' + str(token).encode("ascii", "backslashreplace") + b'|0|0'
        
        return sendData

    def createtoken(self):
        return random.getrandbits(32)
    
    def checkLogin(self, token):
        return token in self.tokenDict.keys()
    
    def getUser(self, user):
        returnUser = None
        for tempUser in self.tokenDict.values():
            if tempUser.User == user:
                returnUser = tempUser
                break
        
        return returnUser
    
    def checkTime(self):
        now = datetime.datetime.now()
        removeUser = []
        for tempUser in self.tokenDict.values():
            tempTime = now - tempUser.lastActive
            seconds = tempTime.total_seconds()
            if seconds > 120:
                removeUser.append(tempUser.Token)

        for token in removeUser:
            del self.tokenDict[token]
    
    def createUser(self, user, hashPass):
        sendData = b'D|R|0|0|0|0'
        if not self.db.verifyUserExists(user):
            self.db.insertUser(user, hashPass, datetime.datetime.now())
            sendData = b'D|R|23|0|0|0'
        else:
            sendData = b'D|R|24|0|0|0'
        return sendData

    def encrypt(self, data, key):
        hexPlaintext = data.hex()
        aesBody = aes(key)
    
        byteList = []
        tempBytes = ""
        encryptedData = ""

        for i in range(len(hexPlaintext)):
            if i % 2 == 0:
                temp = hexPlaintext[i] + hexPlaintext[i + 1]
                tempBytes += temp
        
            if len(tempBytes) == 32:
                byteList.append(tempBytes)
                tempBytes = ""
    
        byteList.append(tempBytes)

        for plaintext in byteList:
            encryptedData += aesBody.encrypt(plaintext)
    
        return encryptedData

    def decrypt(self, cypherText, key):
        aesBody = aes(key)

        tempBytes = ""
        decryptedText = ""
        for i in range(len(cypherText)):
            if i % 2 == 0:
                temp = cypherText[i] + cypherText[i + 1]
                tempBytes += temp
        
            if len(tempBytes) == 32:
                decryptedText += aesBody.decrypt(tempBytes)
                tempBytes = ""

        return decryptedText
    
    def setKey(self, key, address):
        self.keyDict.update({address: key})
        sendData = b'D|R|21|0|0|0'
        return sendData
    

