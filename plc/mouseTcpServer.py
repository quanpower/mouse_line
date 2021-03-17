#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: William Zhang

import sys
import os
from socketserver import TCPServer, StreamRequestHandler, ThreadingTCPServer
from utils import bcd2time, byte2string, checksum, int2bitarray
from PlcConn import plcConn
from SystemStatusLock import query_system_status
from RobotActionLock import in_action, out_action
from camera import trigger_assembly_line_camara, trigger_warehouse_camara, shift_action, camera_trigger
from produce import load_trigger, unload_trigger, in_trigger, out_trigger
from uaServer import ua_main
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
            'white': [7,8,11,12],
            'black': [9,10],
            'grey': []
        },
        'middle': {
            'white': [13,14,17,18],
            'black': [15,16],
            'grey': []                                    
        },
        'up': {
            'white': [19,20],
            'black': [21,22],
            'grey': [23,24]                                    
        },
        'battery': [25],
        'battery_lid': [26],                                 
    },
    'B': {
        'box': [27,28,29,30,31,32], 
        'bottom': {
            'white': [33,34],
            'black': [35,36,37,38],
            'grey': []
        },
        'middle': {
            'white': [39,40],
            'black': [41,42,43,44],
            'grey': []                                    
        },
        'up': {
            'white': [45,46],
            'black': [47,48],
            'grey': [49,50]                                    
        },          
        'battery': [51],
        'battery_lid': [52],                             
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


def return_locator_code(locatorList):
    for j in locatorList:
        index = int(j)
        if not gloVar.wssArray[index-1]:
            return index


def return_position(warehouse, goods, color):
    if goods == 6:
        # box
        position = return_locator_code(warehouse['box'])
    elif goods == 1:
        # bottom
        position = return_locator_code(warehouse['bottom'][color])
    elif goods == 2:
        # middle
        position = return_locator_code(warehouse['middle'][color])
    elif goods == 3:
        # up
        position = return_locator_code(warehouse['up'][color])
    elif goods == 4:
        # battery
        position = return_locator_code(warehouse['battery'])
    elif goods == 5:
        # battery_lid
        position = return_locator_code(warehouse['battery_lid'])
    else:
        print('unknown!')  
        position = 0       
    return position


def return_color_str(color):
    if color == 1:
        color_str = 'black'
    elif color ==2:
        color_str = 'white'
    elif color ==3:
        color_str = 'grey'
    else:
        color_str = 'error'        
    return color_str


class MyThreadingTCPServer(ThreadingTCPServer):
    """重写socketserver.ThreadingTCPServer"""
    # 服务停止后即刻释放端口，无需等待tcp连接断开
    allow_reuse_address = True


class MyTCPHandler(StreamRequestHandler):
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


    ip = ""  
    port = 0  
    timeOut = 180     # 设置超时时间变量 

    def setup(self):  
        self.ip = self.client_address[0].strip()     # 获取客户端的ip  
        self.port = self.client_address[1]           # 获取客户端的port  
        self.request.settimeout(self.timeOut)        # 对socket设置超时时间  
        print(self.ip+":"+str(self.port)+"连接到服务器！")  

    def handle(self):  #所有请求的交互都是在handle里执行的,
        print(self.request)
        print(self.client_address[0])
        client_address = self.client_address[0].strip()  
        print(client_address)
        gloVar.sockets[client_address] = self.request
        print(gloVar.sockets)

        global isNew
        while True:
            try:
                self.data = self.request.recv(1024).strip()
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
                        datalist = data_tuple[1].split(',')   
                        datalist_length = len(datalist)
                        
                        if datalist_length > 6 and datalist_length <= 8:
                            # 2-5相机偏移测量
                            work_station = datalist[0]
                            color = datalist[1]
                            category = datalist[2]
                            ng = datalist[3]

                            print('====ng=====')
                            print(ng)
                            print(int(ng))
                            print(int(ng) == 1)

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
                            if int(ng) == 1:
                            # if 1:
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
                            # 1号相机上料测量普通托盘
                            quantity = int(datalist[0])
                            color = int(datalist[1])
                            category = int(datalist[2])
                            ng = int(datalist[3])
                            print('===ng ====')
                            print(type(ng))
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
                            # if 1:
                                print('==camera data ok!===')
                                positionByte = 2
                                enableByte = 1
                                enableBit = 0
                                enable = 1
                                color_str = return_color_str(color)
                                if category == 1:
                                    warehouse = materials_position['A']
                                    position = return_position(warehouse, goods, color_str)
                                elif category == 2:
                                    warehouse = materials_position['B']
                                    position = return_position(warehouse, goods, color_str) 

                                print('====position===')
                                print(position)

                                if position:
                                    thread_in = threading.Thread(name="thread_in", target=in_action, args=(siemens_1500, positionByte, position, enableByte, enableBit, enable, goods, glock))
                                    thread_in.start()  

                        elif datalist_length >8 :
                            # 1号相机上料测量电池盖
                            print('===b_ ====')
                            b_quantity = int(datalist[0])
                            b_color = int(datalist[1])
                            b_category = int(datalist[2])
                            b_ng = int(datalist[3])
                            b_goods = int(datalist[4])

                            print('===w_ ====')
                            w_quantity = int(datalist[5])
                            w_color = int(datalist[6])
                            w_category = int(datalist[7])
                            w_ng = int(datalist[8])
                            w_goods = int(datalist[9])

                            print('=======camera1========')

                            if b_ng == 1 and  w_ng == 1:
                            # if 1:
                                print('==battery_lid camera data ok!===')
                                positionByte = 2
                                enableByte = 1
                                enableBit = 0
                                enable = 1

                                # 26,52
                                position = return_locator_code([26, 52])
                                print('====position===')
                                print(position)

                                if position:
                                    thread_in = threading.Thread(name="thread_in", target=in_action, args=(siemens_1500, positionByte, position, enableByte, enableBit, enable, goods, glock))
                                    thread_in.start()                                      
                    else:
                        print('unhandled!')
                        print(data_tuple)
                        action_list = []

            except ConnectionResetError as e:
                print("err", e)
                break

    def finish(self):  
        print(self.ip+":"+str(self.port)+"断开连接！")  
        # 断开时删除本socket
        # client_sockets.pop(self.ip)

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

        # 循环读取待产订单，准备生产
        thread_load_trigger = threading.Thread(name='thread_load_trigger', target=load_trigger, args=(glock,))
        thread_load_trigger.start()

        # 循环读取下料订单，准备下料
        thread_unload_trigger = threading.Thread(name='thread_unload_trigger', target=unload_trigger, args=(glock,))
        thread_unload_trigger.start()

        # 循环读取生产订单，上报opc ua server
        thread_ua_main = threading.Thread(name='thread_ua_main', target=ua_main)
        thread_ua_main.start()        

        HOST, PORT = "172.16.6.250", 8000 #windows

        server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)   #线程
        server.serve_forever()

    except KeyboardInterrupt as e:
        print(e)
        #print '^C received, shutting down server'
        server.socket.close()