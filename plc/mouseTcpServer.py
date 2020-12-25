#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: William Zhang

import sys
import os
from socketserver import TCPServer, StreamRequestHandler
from utils import bcd2time, byte2string, checksum, int2bitarray
from PlcConn import plcConn
from SystemStatusLock import query_system_status
from RobotActionLock import in_action, out_action
from camera import trigger_assembly_line_camara, trigger_warehouse_camara, shift_action, camera_trigger
from laser_client import client_send
import threading 
import traceback
import time
import struct
import binascii
import logging

import socketserver


# 导入全局变量
from global_list import gloVar

BUFSIZE = 4096


materials_position = {
    'A': {
        'box': [1,2,3,4,5,6],
        'bottom': {
            'black': [7,8],
            'white': [9,10],
            'pink': [11,12]
        },
        'middle': {
            'black': [13,14],
            'white': [15,16],
            'pink': [17,18]                                    
        },
        'up': {
            'black': [19,20],
            'white': [21,22],
            'pink': [23,24]                                    
        }                                
    },
    'B': {
        'box': [27,28,29,30,31,32],
        'bottom': {
            'black': [33,34],
            'white': [35,36],
            'pink': [37,38]
        },
        'middle': {
            'black': [39,40],
            'white': [41,42],
            'pink': [43,44]                                    
        },
        'up': {
            'black': [45,46],
            'white': [47,48],
            'pink': [49,50]                                    
        },    
        'battery': [25, 26],
        'battery_lid': [51,52],                             
    }
}


logging.basicConfig(
    # 日志级别,logging.DEBUG,logging.ERROR
    # level = logging.WARNING,  
    level = logging.INFO,  
    # 日志格式
    # 时间、代码所在文件名、代码行号、日志级别名字、日志信息
    format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    # 打印日志的时间
    datefmt = '%a, %Y-%m-%d %H:%M:%S',
    # 日志文件存放的目录（目录必须存在）及日志文件名
    filename = 'TcpserverReport.log',
    # 打开日志文件的方式
    filemode = 'w'
)


def logger(log_obj):
    logger = logging.getLogger(log_obj)
    logger.setLevel(logging.INFO)
    console_handle = logging.StreamHandler()
    log_file = "access.log"
    file_handle = logging.FileHandler(log_file)
    file_handle.setLevel(logging.WARNING)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    console_handle.setFormatter(formatter)
    file_handle.setFormatter(formatter)

    logger.addHandler(console_handle)
    logger.addHandler(file_handle)

    return logger

def return_position(warehouse, goods, color):
    if goods == 6:
        # box
        position = warehouse['box'][0]
    elif goods == 3:
        # bottom
        position = warehouse['bottom'][color][0]
    elif goods == 2:
        # middle
        position = warehouse['middle'][color][0]
    elif goods == 1:
        # up
        position = warehouse['up'][color][0]
    elif goods == 4:
        # battery
        position = warehouse['battery'][0]
    elif goods == 5:
        # battery_lid
        position = warehouse['battery_lid'][0]
    else:
        print('unknown!')  
        position = 0       
    return position


class MyTCPHandler(socketserver.BaseRequestHandler):
    # def __init__(self, socket, host_port, server):
    #     self.server = server
    #     self.socket = socket
    #     print(host_port)
    #     (self.host, self.port) = self.socket.getpeername()
    #     print(self.host)
    #     print(self.port)
    #     client_address = self.host
    #     print(client_address)
    #     # gloVar.sockets[client_address] = self.socket

    #     # print(gloVar.sockets)

    def handle(self):  #所有请求的交互都是在handle里执行的,
        print(self.request)
        print(self.client_address[0])
        client_address = self.client_address[0]
        print(client_address)
        gloVar.sockets[client_address] = self.request
        print(gloVar.sockets)

        global isNew
        while True:
            try:
                self.data = self.request.recv(1024).strip()#每一个请求都会实例化MyTCPHandler(socketserver.BaseRequestHandler):
                siemens_1500 = gloVar.siemens_1500

                if len(self.data) < 1:
                    pass
                else:
                    print('\n' * 5)
                    print(self.data)
                    data_tuple = self.data.strip().decode("utf-8").split(';')
    
                    if 'laser' == data_tuple[0]:
                        print('===laser begin!====')
                        data = data_tuple[1]
                        print(data)
                        print(len(data))
                        if len(data) > 2:
                            thread_laser = threading.Thread(name="thread_laser", target=client_send, args=(data,))
                            thread_laser.start()    

                    elif 'Camera' == data_tuple[0]:
                        print('===camera begin!====')
                        data = data_tuple[1]
                        print(data)
                        # thread_laser = threading.Thread(name="thread_laser", target=client_send, args=(data,))
                        # thread_laser.start()  
                        datalist = data_tuple[1].split(',')   
                        datalist_length = len(datalist)
                        
                        if datalist_length > 6:
                            work_station = datalist[0]
                            color = datalist[1]
                            category = datalist[2]
                            ng = datalist[3]
                            shift_x = datalist[4]
                            shift_y = datalist[5]
                            shift_a = datalist[6]
                            print('========camera2=========')
                            print(work_station)
                            print(color)
                            print(category)
                            print(ng)
                            print(shift_x)
                            print(shift_y)
                            print(shift_a)

                            # ng==1 ,success
                            # if int(ng) == 1:
                            if 1:
                                if int(work_station) == 1:
                                    shiftxByte= 46
                                    shiftyByte = 50
                                    shiftaByte = 54
                                    shiftxValue = float(shift_x)
                                    shiftyValue = float(shift_y)
                                    shiftaValue = float(shift_a)
                                    enableByte = 1
                                    enableBit = 1
                                    enableValue = 1 

                                elif int(work_station) == 2:
                                    shiftxByte= 58
                                    shiftyByte = 62
                                    shiftaByte = 66
                                    shiftxValue = float(shift_x)
                                    shiftyValue = float(shift_y)
                                    shiftaValue = float(shift_a)
                                    enableByte = 1
                                    enableBit = 2
                                    enableValue = 1 

                                elif int(work_station) == 3:
                                    shiftxByte= 70
                                    shiftyByte = 74
                                    shiftaByte = 78
                                    shiftxValue = float(shift_x)
                                    shiftyValue = float(shift_y)
                                    shiftaValue = float(shift_a)
                                    enableByte = 1
                                    enableBit = 3
                                    enableValue = 1 

                                elif int(work_station) == 4:
                                    shiftxByte= 82
                                    shiftyByte = 86
                                    shiftaByte = 90
                                    shiftxValue = float(shift_x)
                                    shiftyValue = float(shift_y)
                                    shiftaValue = float(shift_a)
                                    enableByte = 1
                                    enableBit = 4
                                    enableValue = 1 
   
                                thread_shift = threading.Thread(name="thread_shift", target=shift_action, args=(siemens_1500, shiftxByte, shiftxValue, shiftyByte, shiftyValue, shiftaByte, shiftaValue,enableByte, enableBit, enableValue, glock))
                                thread_shift.start()

                        elif datalist_length <= 6 and datalist_length >=3:
                            quantity = int(datalist[0])
                            color = int(datalist[1])
                            category = int(datalist[2])
                            ng = int(datalist[3])
                            goods = int(datalist[4])

                            print('=======camera1========')
                            logger.info('=====camera1=====')

                            print(quantity)
                            print(color)
                            print(category)
                            print(ng)
                            print(goods)
                            logger.info(quantity)
                            logger.info(color)
                            logger.info(category)
                            logger.info(ng)
                            logger.info(goods)
                            # ng==1 ,success
                            if ng == 1:
                                print('camera data ok!')
                                positionByte = 2
                                enableByte = 1
                                enableBit = 0
                                enable = 1

                                if category == 1:
                                    warehouse = materials_position['A']
                                    position = return_position(warehouse, goods, color)
                                elif category == 0:
                                    warehouse = materials_position['B']
                                    position = return_position(warehouse, goods, color) 

                                if position != 0:
                                    thread_in = threading.Thread(name="thread_in", target=in_action, args=(siemens_1500, positionByte, position, enableByte, enableBit, enable, glock))
                                    thread_in.start()   

                    elif 'produce' == data_tuple[0]:
                        data = data_tuple[1]
                        datalist = data_tuple[1].split(',')  

                        model = datalist[0]
                        color = datalist[1]
                        no = datalist[2]


                        if model == 'A':
                            warehouse = materials_position['A']
                            box_p = warehouse['box'][0]
                            bottom_p = warehouse['bottom'][color][0]
                            middle_p = warehouse['middle'][color][0]
                            up_p = warehouse['up'][color][0]
                            out_list = [box_p, bottom_p, middle_p, up_p]
                        elif model == 'B':
                            warehouse = materials_position['B']
                            box_p = warehouse['box'][0]
                            bottom_p = warehouse['bottom'][color][0]
                            middle_p = warehouse['middle'][color][0]
                            up_p = warehouse['up'][color][0]
                            battery_p = warehouse['battery'][0]
                            battery_lid_p = warehouse['battery_lid'][0]

                            out_list = [box_p, bottom_p, middle_p, up_p, battery_p, battery_lid_p]
                        else:
                            out_list = []

                        out_list = [7,13,19,3]
                        # out_list = [7,13,19]
                        out_lists = [
                            [
                            {'position':7,
                            'no':1,
                            'quantity':6
                            },
                            {'position':13,
                            'no':1,
                            'quantity':6
                            },
                            {'position':19,
                            'no':1,
                            'quantity':6
                            },
                            {'position':3,
                            'no':1,
                            'quantity':6
                            } 
                        ],[
                            {'position':7,
                            'no':2,
                            'quantity':5
                            },
                            {'position':13,
                            'no':2,
                            'quantity':5
                            },
                            {'position':19,
                            'no':2,
                            'quantity':5
                            },
                            {'position':3,
                            'no':2,
                            'quantity':5
                            } 
                        ],[
                            {'position':7,
                            'no':3,
                            'quantity':4
                            },
                            {'position':13,
                            'no':3,
                            'quantity':4
                            },
                            {'position':19,
                            'no':3,
                            'quantity':4
                            },
                            {'position':3,
                            'no':3,
                            'quantity':4
                            } 
                        ],
                        ],
                        out_list = out_lists[int(no)]
                        print(out_list)

                        positionByte = 6
                        noByte = 94
                        quantityByte = 96
                        enableByte = 4
                        enableBit = 0
                        enable = 1
                        if out_list:
                            thread_out = threading.Thread(name="thread_out", target=out_action, args=(siemens_1500, positionByte,noByte,quantityByte, enableByte, enableBit, enable,out_list, glock))
                            thread_out.start()

                    elif 'trigger2' == data_tuple[0]:
                        triggerCtl = 'A101'
                        thread_trigger = threading.Thread(name="thread_trigger", target=trigger_assembly_line_camara, args=('192.168.0.111', triggerCtl))
                        thread_trigger.start()                     

                    else:
                        print('unhandled!')
                        print(data_tuple)
                        action_list = []

            except ConnectionResetError as e:
                print("err ",e)
                break


if __name__ == "__main__":

    logger = logging.getLogger(__name__)

    try:
        logger.info('registered user, welcome to use!')

        glock=threading.Lock()

        thread_plcConn = threading.Thread(name='thread_plcConn', target=plcConn)
        thread_statusRead_0 = threading.Thread(name='thread_statusRead_0', target=query_system_status, args=(glock,))
        # 连接PLC
        thread_plcConn.start()
        time.sleep(5)
        # 循环读取PLC及机器人状态
        thread_statusRead_0.start()

        # 循环读取触发信号
        thread_camera_trigger = threading.Thread(name='thread_camera_trigger', target=camera_trigger)
        thread_camera_trigger.start()

        HOST, PORT = "172.16.6.250", 8000 #windows
        # HOST, PORT = "192.168.0.200", 8000 #windows
        # HOST, PORT = "0.0.0.0", 8000 #windows
        # HOST, PORT = "192.168.8.251", 8000 #windows

        server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)   #线程
        server.serve_forever()

    except KeyboardInterrupt as e:
        print(e)
        #print '^C received, shutting down server'
        server.socket.close()