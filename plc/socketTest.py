import socket
import time

ip = '192.168.8.100'
port = 8000

server_socket = socket.socket()
server_socket.bind((ip, port))
server_socket.listen()
client_socket, client_addr = server_socket.accept()
print("接收到客户端{}的请求,端口{}".format(client_addr[0], client_addr[1]))

while 1:

    data = client_socket.recv(1024)
    if data:
        print("----->客服端发来的数据{}".format(data.decode('utf-8')))
        client_socket.send(data)
    else:
        print('no data!')
        break
    time.sleep(1)

print("发送完成")

server_socket.close()