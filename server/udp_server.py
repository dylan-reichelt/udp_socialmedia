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
            tempUser.Token = token
            tempUser.address = address
            tempUser.lastActive = datetime.datetime.now()

            self.tokenList.append(token)
            self.onlineUsers.append(tempUser)
            returnMe = sendData = b'D|R|03|' + str(token).encode("ascii", "backslashreplace") + b'|0|0'
            return returnMe
        else:
            returnMe = b'D|R|04|0|0|0'
            return returnMe
    
    def createtoken(self):
        return random.getrandbits(32)
    
    def checkLogin(self, token):
        logged = False
        
        if token in self.tokenList:
            logged = True

        return logged
