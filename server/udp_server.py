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
            return True
        else:
            return False
    
    def createtoken(self):
        return random.getrandbits(32)


"""
while True:
    print('\nwaiting to receive message')
    data, address = sock.recvfrom(4096)

    print('received {} bytes from {}'.format(len(data), address))
    print(data)

    if data:
        sent = sock.sendto(data, address)
        print('sent {} bytes back to {}'.format(sent, address))
"""