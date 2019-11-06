import socket
import sys

class Server:
    def __init__(self):
        userDict = {"dylan" : "programmer",
                    "alex" : "loser",
                    "max" : "gamer"}

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