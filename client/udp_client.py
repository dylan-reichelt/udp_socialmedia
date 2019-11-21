import socket
import sys

from aes_encryption import aes

class Client:
    def __init__(self, server, key):

        # Create a UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = (server, 10000)

        # Sending key for encryption and decryption
        self.key = key
        keyPayload = b'D|R|20|0|0|' + str(self.key).encode("ascii", "backslashreplace")

        self.sock.sendto(keyPayload, self.server_address)
    
    def send(self, sendData):
        sendData = self.encrypt(sendData).encode("ascii", "backslashreplace")
        self.sock.sendto(sendData, self.server_address)
    
    def listen(self):
        data, server = self.sock.recvfrom(4096)
        data = self.decrypt(data.decode("utf-8"))
        return [data, server]
    
    def encrypt(self, data):
        hexPlaintext = data.hex()
        aesBody = aes(self.key)
    
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

    def decrypt(self, cypherText):
        aesBody = aes(self.key)

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

