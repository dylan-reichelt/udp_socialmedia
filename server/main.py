from udp_server import Server


def main():
    udpServer = Server()

    while True:
        data, address = udpServer.listen()

        if data:
            action, info = data.decode("utf-8").split("#")

            if action == "login":
                user, password = info.split("&")
                udpServer.logon(user, password, address)
                sent = udpServer.send(b'LOGIN SUCCESSFUL', address)
            else:
                sent = udpServer.send(b'ERROR: not a recognized command', address)


if __name__ == "__main__":
    main()
