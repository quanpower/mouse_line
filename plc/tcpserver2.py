#coding:utf-8
from socketserver import TCPServer,BaseRequestHandler
import traceback
from matrix2quat import euler2quat,quat2euler,matrix2quat,matrix2euler
import struct

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

class MyBaseRequestHandler(BaseRequestHandler):
    """
    #继承BaseRequestHandler的handle方法
    """
    def handle(self):
        global isNew
        global stringSendToRobot
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


if __name__ == "__main__":

    global isNew 
    global stringSendToRobot 

    isNew = False
    stringSendToRobot = b'0,0,0,0,0,0,0,0'

    # 开启ip和端口
    ip_port = ("192.168.8.100", 8000)
    #构造TCPServer对象
    server = TCPServer(ip_port,MyBaseRequestHandler)
    #启动服务器监听
    server.serve_forever()