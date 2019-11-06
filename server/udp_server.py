import socket
import sys
import random
import datetime

from user import User


class Server:
    def __init__(self):
        self.userDict = {"dylan" : "programmer",
                    "alex" : "loser",
                    "max" : "gamer"}
        
        self.onlineUsers = []
        self.tokenList = []

        # Creates a UDP Socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Bind the socket to the port
        self.server_address = ('localhost', 10000)
        self.sock.bind(self.server_address)

    def listen(self):
        print('\nwaiting to receive message')
        data, address = self.sock.recvfrom(4096)
        return [data, address]
    
    def send(self, data, address):
        return self.sock.sendto(data, address)
    
    def logon(self, name, password, address):

        #logon successful name and password match
        if name in self.userDict.keys() and self.userDict[name] == password:
            
            token = 0
            while True:
                token = self.createtoken()
                if token not in self.tokenList:
                    break
            

            tempUser = User()
            tempUser.User = name
            tempUser.Online = True
            tempUser.Token = str(token)
            tempUser.address = address
            tempUser.lastActive = datetime.datetime.now()

            self.tokenList.append(str(token))
            self.onlineUsers.append(tempUser)
            sendData = b'D|R|03|' + str(token).encode("ascii", "backslashreplace") + b'|0|0'
            return sendData
        else:
            sendData = b'D|R|04|0|0|0'
            return sendData
        
    def subscribe(self, user, token):
        sendData = b'D|R|0|0|0|0'
        if self.checkLogin(token):
            print("DO SOMETHING")
        else:
            sendData = b'D|R|01|' + str(token).encode("ascii", "backslashreplace") + b'|0|0'
            
        return sendData
    
    def createtoken(self):
        return random.getrandbits(32)
    
    def checkLogin(self, token):
        return token in self.tokenList
