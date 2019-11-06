from udp_client import Client
from time import sleep
import threading

client = Client('localhost')
canSend = True
Token = 0

def sendLoop():

    while True:
        # Send data
        message = input()
        global Token
        print(Token)
        action, data = message.split("#")
        global canSend
        if action and canSend:
            if action == "login":
                sendData = b'D|R|02|0|0|' + str(data).encode("ascii", "backslashreplace")
                sent = client.send(sendData)
                canSend = False
            else:
                print("ERROR: Not a recognized command")

def listenLoop():
    global canSend
    global Token 
    while True:
        tempData, server = client.listen()
        data = tempData.decode("ascii")
        dataSplit = data.split("|")
        firstInitial = dataSplit[0]
        secondInitial = dataSplit[0]
        opcode = dataSplit[2]
        tempToken = dataSplit[3]
        messageID = dataSplit[4]
        payload = dataSplit[5]

        if opcode == "03":
            print("login_ack#successful")
            Token = tempToken
        elif opcode == "04":
            print("login_ack#failed")
        else:
            print("ERROR: unable to read opcode")

        canSend = True

thread = threading.Thread(target = listenLoop)
thread.daemon = True
thread.start()


if __name__ == "__main__":
    sendLoop()