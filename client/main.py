from udp_client import Client
from time import sleep
import threading
import hashlib

client = Client('localhost')
canSend = True
Token = 0

def sendLoop():

    while True:
        message = input()
        global Token
        action, data = message.split("#")
        global canSend

        if action and canSend:
            if action == "login":

                # Hashing Password so no plaintext pass is sent over the network
                str(data).encode("ascii", "backslashreplace")
                user, plainPass = data.split("&")
                binPlainPass = plainPass.encode("ascii", "backslashreplace")
                hashpass = hashlib.sha256(binPlainPass).hexdigest()

                # Setting the data back to the user and now hashpass
                data = user + "&" + hashpass
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

            elif action == "post":
                sendData = b'D|R|11|' + str(Token).encode("ascii", "backslashreplace") + b'|0|' + str(data).encode("ascii", "backslashreplace")
                send = client.send(sendData)
                canSend = False

            elif action == "retrieve":
                sendData = b'D|R|15|' + str(Token).encode("ascii", "backslashreplace") + b'|0|' + str(data).encode("ascii", "backslashreplace")
                send = client.send(sendData)
                canSend = False

            elif action == "logout":
                sendData = b'D|R|18|' + str(Token).encode("ascii", "backslashreplace") + b'|0|' + str(data).encode("ascii", "backslashreplace")
                send = client.send(sendData)
                canSend = False

            else:
                print("ERROR: Not a recognized action resetting...")

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
        elif opcode == "12":
            print("post_ack#successful")
        elif opcode == "13":
            print(str(payload))
            sendData = b'D|R|14|' + str(Token).encode("ascii", "backslashreplace") + b'|0|0'
            send = client.send(sendData)
        elif opcode == "16":
            print(str(payload))
        elif opcode == "17":
            print("retrieve_ack#successful")
        elif opcode == "19":
            print("logout_ack#successful")
        else:
            print("ERROR: unrecognized opcode resetting...")

        canSend = True

thread = threading.Thread(target = listenLoop)
thread.daemon = True
thread.start()


if __name__ == "__main__":
    sendLoop()