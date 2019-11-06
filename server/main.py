from udp_server import Server


def main():
    udpServer = Server()

    while True:
        data, address = udpServer.listen()

        if data:
            dataSplit = data.decode("utf-8").split("|")

            firstInitial = dataSplit[0]
            secondInitial = dataSplit[1]
            opcode = dataSplit[2]
            Token = dataSplit[3]
            messageID = dataSplit[4]
            payload = dataSplit[5]
            
            if opcode == "02":
                user, password = payload.split("&")
                ack = udpServer.logon(user, password, address)
                sent = udpServer.send(ack, address)
            elif opcode == "05":
                ack = udpServer.subscribe(payload, Token)
                send = udpServer.send(ack, address)
            elif opcode == "08":
                ack = udpServer.unsubscribe(payload, Token)
                send = udpServer.send(ack, address)
            elif opcode == "11":
                ack = udpServer.post(payload, Token)
                send = udpServer.send(ack, address)

if __name__ == "__main__":
    main()
