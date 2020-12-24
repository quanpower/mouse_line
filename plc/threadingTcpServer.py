#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao

import socketserver
from matrix2quat import euler2quat,quat2euler,matrix2quat,matrix2euler
import struct

def dataProcess(data):
    global stringSendToRobot
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


class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):  #所有请求的交互都是在handle里执行的,
        global isNew
        global stringSendToRobot

        while True:
            try:
                self.data = self.request.recv(1024).strip()#每一个请求都会实例化MyTCPHandler(socketserver.BaseRequestHandler):
                print("{} wrote:".format(self.client_address[0]))
                print(self.data)

                if len(self.data) < 5:
                    break
                else:
                    if len(self.data) == 200:
                        print('get data from camera!')
                        isNew = True
                        print('======set isNew=======')
                        dataProcess(self.data)
                        break

                    elif 'robot' in self.data.strip()[:10].decode("utf-8"):
                        print('\n' * 5)
                        print('get data from robot!')
                        print('======isNew====')
                        print(isNew)

                        if isNew:
                            print('====stringSendToRobot=====')
                            print(stringSendToRobot)
                            isNew = False
                            bytesToRobot = stringSendToRobot.encode(encoding="utf-8")
                            self.request.sendall(bytesToRobot)
                        else:
                            self.request.sendall(b'0,0,0,0,0,0,0,0')
                    else:
                        print('unhandled!')
            except ConnectionResetError as e:
                print("err ",e)
                break

if __name__ == "__main__":

    global isNew 
    global stringSendToRobot 

    isNew = False
    stringSendToRobot = b'0,0,0,0,0,0,0,0'

    HOST, PORT = "192.168.8.100", 8000 #windows
    try:
        server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)   #线程
        server.serve_forever()
    except KeyboardInterrupt as e:
        print(e)
        #print '^C received, shutting down server'
        server.socket.close()