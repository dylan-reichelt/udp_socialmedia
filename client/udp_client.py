

import socket
import sys

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 10000)
#message = b'login#dylan&programmer'

try:

    while True:
        # Send data
        message = input().encode("ascii", "backslashreplace")
        if message:
            print('sending {!r}'.format(message))
            sent = sock.sendto(message, server_address)

            # Receive response
            print('waiting to receive')
            data, server = sock.recvfrom(4096)
            print('received: ', data)

finally:
    print('closing socket')
    sock.close()

