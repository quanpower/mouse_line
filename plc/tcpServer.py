import socket, threading, random
import re
import struct

from matrix2quat import euler2quat,quat2euler,matrix2quat,matrix2euler

def dataProcess(data):
    dataArrary = data.split(b',')
    print(dataArrary)
    matrix = dataArrary[:17]
    x = matrix[4].decode("utf-8")
    y = matrix[8].decode("utf-8")
    z = matrix[12].decode("utf-8")
    trans = [x,y,z]
    print(trans)

    l1 = matrix[1:4]
    l2 = matrix[5:8]
    l3 = matrix[9:12]
    rMatrix = [l1,l2,l3]
    print(rMatrix)

    quat = matrix2quat(rMatrix)
    print(quat)

    # list2robot = list()
    # list.append('1')
    # print(list2robot)
    list2robot = ['1',]
    print(list2robot)
    print(type(list2robot))
    list2robot.extend(trans)
    list2robot.extend(quat)
    # trans.extend(quat)
    print('=====list2robot====')
    print(list2robot)
    stringSendToRobot = ','.join(list2robot)
    print('======stringSendToRobot======')
    print(stringSendToRobot)


# 要发送的机器人坐标数据，用数组保存起来，随机发送
send_recv = ["72.12,100,100", "-127.12,78,60", "50.12,121,50", "100.12,90,56", "133.12,60,47"]


def recv_data(new_socket):
    global isNew
    global stringSendToRobot
    
    while True:
        try:
            data = self.request.recv(1024).strip()
            # data = self.request.recv(1024).strip().decode("utf-8")
            print('\n' * 5)
            print("receive for(%r):%r"%(self.client_address,data))                
            # if 'camera' in data.strip()[:10].decode("utf-8"):
            if len(data) == 200:
                print('get data from camera!')
                isNew = True
                print('set isNew')
                dataProcess(data)
                break

            elif 'robot' in data.strip()[:10].decode("utf-8"):
                print('get data from robot!')
                if isNew:
                    self.request.sendall(stringSendToRobot)
                    isNew = False
                else:
                    self.request.sendall(b'0,0,0,0,0,0,0,0')
        except Exception as e:
            print(e)  

    new_socket.close()


    def handle(self):

        while True:
           #当客户端主动断开连接时候，self.recv(1024)会抛出异常
            try:
                data = self.request.recv(1024).strip()
                # data = self.request.recv(1024).strip().decode("utf-8")

                print('\n' * 5)
                print("receive for(%r):%r"%(self.client_address,data))                
                # if 'camera' in data.strip()[:10].decode("utf-8"):
                if len(data) == 200:
                    print('get data from camera!')
                    isNew = True
                    print('set isNew')
                    dataProcess(data)
                    break

                elif 'robot' in data.strip()[:10].decode("utf-8"):
                    print('get data from robot!')
                    if isNew:
                        self.request.sendall(stringSendToRobot)
                        isNew = False
                    else:
                        self.request.sendall(b'0,0,0,0,0,0,0,0')
                    
            except:
                traceback.print_exc()
                break



def main():
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    socket_server.bind(('192.168.8.100', 8000))
    # 182.168.125.10
    socket_server.listen(128)
    while True:
        try:
            new_socket, ip_port = socket_server.accept()
        except:
            pass
        else:
            a, b = ip_port
            print(f"连线成功,客户端IP：{a} 端口：{b}")
            t = threading.Thread(target=recv_data, args=(new_socket,))
            t.start()

    # socket_server.close()

if __name__ == "__main__":
    main()
