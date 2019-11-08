import socket
import sys

class Client:
    def __init__(self, server):

        # Create a UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = (server, 10000)
    
    def send(self, sendData):
        self.sock.sendto(sendData, self.server_address)
    
    def listen(self):
        data, server = self.sock.recvfrom(4096)
        return [data, server]

