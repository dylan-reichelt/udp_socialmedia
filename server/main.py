from udp_server import Server

def main():
    udpServer = Server()

    while True:
        data, address = udpServer.listen()

        if data:
            dataSplit = data.split("|")

            firstInitial = dataSplit[0]
            secondInitial = dataSplit[1]
            opcode = dataSplit[2]
            Token = dataSplit[3]
            messageID = dataSplit[4]
            payload = dataSplit[5]

            udpServer.checkTime()
            
            if opcode == "02":
                user, password = payload.split("&")
                ack = udpServer.logon(user, password, address)
                udpServer.send(ack, address)

            elif opcode == "05":
                ack = udpServer.subscribe(payload, Token)
                udpServer.send(ack, address)

            elif opcode == "08":
                ack = udpServer.unsubscribe(payload, Token)
                udpServer.send(ack, address)

            elif opcode == "11":
                ack = udpServer.post(payload, Token)
                udpServer.send(ack, address)

            elif opcode == "15":
                number = int(payload)
                ack = udpServer.retrieve(Token, number)
                udpServer.send(ack, address)

            elif opcode == "18":
                ack = udpServer.logout(Token)
                udpServer.send(ack, address)

            elif opcode == "20":
                ack = udpServer.setKey(payload, address)
                udpServer.send(ack, address)

            else:
                print("Resetting...")

if __name__ == "__main__":
    main()
