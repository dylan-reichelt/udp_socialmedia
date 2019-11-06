from udp_server import Server


def main():
    testServer = Server()

    while True:
        data, address = testServer.listen()
        print('received {} bytes from {}'.format(len(data), address))
        print(data)

        if data:
            sent = testServer.send(data, address)
            print('sent {} bytes back to {}'.format(sent, address))

if __name__ == "__main__":
    main()
