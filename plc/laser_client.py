import socket
import sys

HOST, PORT = "172.16.6.250", 6000


def client_send(data):
    # Create a socket (SOCK_STREAM means a TCP socket)

    print('=====laser begin in socket======')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        # sock.sendall(bytes(data + "\n", "utf-8"))
        sock.sendall(bytes(data + "\n", "gb2312"))

        # Receive data from the server and shut down
        received = str(sock.recv(1024), "gb2312")

    print("Sent:     {}".format(data))
    print("Received: {}".format(received))