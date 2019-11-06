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
        action, data = message.split("#")
        global canSend
        if action and canSend:
            if action == "login":
                sendData = b'D|R|02|' + str(Token).encode("ascii", "backslashreplace") + b'|0|' + str(data).encode("ascii", "backslashreplace")
                sent = client.send(sendData)
                canSend = False
            elif action == "subscribe":
                sendData = b'D|R|05|' + str(Token).encode("ascii", "backslashreplace") + b'|0|' + str(data).encode("ascii", "backslashreplace")
                send = client.send(sendData)
                canSend = False
            elif action == "unsubscribe":
                sendData = b'D|R|08|' + str(Token).encode("ascii", "backslashreplace") + b'|0|' + str(data).encode("ascii", "backslashreplace")
                send = client.send(sendData)
                canSend = False
            else:
                print("ERROR: Not a recognized action")

def listenLoop():
    global canSend
    global Token 
    while True:
        tempData, server = client.listen()
        data = tempData.decode("ascii")
        dataSplit = data.split("|")
        firstInitial = dataSplit[0]
        secondInitial = dataSplit[1]
        opcode = dataSplit[2]
        tempToken = dataSplit[3]
        messageID = dataSplit[4]
        payload = dataSplit[5]

        if opcode == "03":
            print("login_ack#successful")
            Token = tempToken
        elif opcode == "04":
            print("login_ack#failed")
        elif opcode == "01":
            print("ERROR: login to perform this action!")
        elif opcode == "06":
            print("subscribe_ack#successful")
        elif opcode == "07":
            print("subscribe_ack#failed")
        elif opcode == "09":
            print("unsubscribe_ack#successful")
        elif opcode == "10":
            print("unsubscribe_ack#failed")
        else:
            print("ERROR: unrecognized opcode")

        canSend = True

thread = threading.Thread(target = listenLoop)
thread.daemon = True
thread.start()


if __name__ == "__main__":
    sendLoop()