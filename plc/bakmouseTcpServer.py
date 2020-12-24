#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: William Zhang

import sys
import os
from socketserver import TCPServer, StreamRequestHandler
from utils import bcd2time, byte2string, checksum, int2bitarray
from PlcConn import plcConn
from SystemStatusLock import query_system_status
from RobotActionLock import warehouse_input, warehouse_output
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


class MyStreamRequestHandler(StreamRequestHandler):
    """
    #继承StreamRequestHandler，并重写handle方法
    #（StreamRequestHandler继承自BaseRequestHandler）
    """

    class MsgStruct(object):
        """
        MsgStruct
        """
        def __init__(self, version, msg_time, seq, ctl, msg_length, msg_data, cs):
            self.SOF = 0x68
            self.Version = version
            self.Time = msg_time
            self.SEQ = seq
            self.SFD = 0x68
            self.CTL = ctl
            self.LEN = msg_length
            self.DATA = msg_data
            self.CS = cs
            self.EOF = 0x16


        def isCsRight(self, cs, msg_list_pre):
            return cs == checksum(msg_list_pre)

        def returnBytesList(self, ctl, data):
            # low = len(data)%256
            # high = len(data)//256
            high, low = divmod(len(data), 256)
            time_now = time.localtime(time.time())

            msgList = []
            msgList.append(self.SOF)
            msgList.append(self.Version[0])
            msgList.append(self.Version[1])
            msgList.append(time_now[0]-2000)
            msgList.append(time_now[1])
            msgList.append(time_now[2])
            msgList.append(time_now[3])
            msgList.append(time_now[4])
            msgList.append(time_now[5])
            msgList.append(self.SEQ)
            msgList.append(self.SFD)
            msgList.append(ctl)

            msgList.append(low)
            msgList.append(high)

            for i in data:
                msgList.append(i)
            # print(msgList)
            list_cs = checksum(msgList)
            msgList.append(list_cs)
            msgList.append(self.EOF)

            if len(data) > 0:
                return_bytes = struct.pack('1B2B6B1B1B1B2B' + str(len(data)) +'B1B1B', *msgList)
            else:
                return_bytes = struct.pack('1B2B6B1B1B1B2B1B1B', *msgList)
            # logger.info('return_bytes:', return_bytes)
            return return_bytes

    def work_dispatch(self):
        self.msg_list_pre = self.msg_list[:-2]
        # logger.info('msg_list:' + str(self.msg_list))
        # logger.info(self.msg_list_pre)
        # logger.info(checksum(self.msg_list_pre))

        #获取socket句柄
        siemens_1500 = gloVar.siemens_1500

        version = self.msg_list[1:3]
        msg_time = self.msg_list[3:9]
        seq = self.msg_list[9]
        ctl = self.msg_list[11]
        msg_length = self.msg_list[12:14]
        msg_data = self.msg_list[14:-2]
        cs=self.msg_list[-2]

        self.request_struct = self.MsgStruct(version, msg_time, seq, ctl, msg_length, msg_data, cs)
        # logger.info(self.request_struct.isCsRight(cs, self.msg_list_pre))

        if ctl == 0x01:
            """
                login
            """
            logger.info('loged in')

            login_ack = self.request_struct.returnBytesList(0x81, [])
            self.response = login_ack

        elif ctl == 0x02:
            """
                quit
            """
            logger.info('quited!')

            quit_ack = self.request_struct.returnBytesList(0x82, [])
            self.response = quit_ack
            self.REQUEST_QUIT = True

        elif ctl == 0x03:
            """
                heart beat, break if haven't receive heart beat more than 6 minute
            """
            logger.info('\n' * 5)
            logger.info('-----heart beating...---------')

            heart_beat_ack = self.request_struct.returnBytesList(0x83, [])
            self.response = heart_beat_ack

        elif ctl == 0x10:
            """
                query system status
            """
            # logger.info('-----system_status-----')
            robot_addr = self.request_struct.DATA[0] 

            # logger.info('-----gloVar.system_status_global-----')
            # logger.info(robot_addr)
            # logger.info(gloVar.robot_0_system_status_global)
            # logger.info(gloVar.robot_1_system_status_global)

            if robot_addr == 0:
                # robot_0_system_status()  
                system_status_ack = self.request_struct.returnBytesList(0x90, gloVar.robot_0_system_status_global)       

            elif robot_addr == 1:
                # robot_1_system_status() 
                system_status_ack = self.request_struct.returnBytesList(0x90, gloVar.robot_1_system_status_global)

            self.response = system_status_ack  
            # logger.info('---system_status_ack response----')          
            # logger.info(self.response)          

        elif ctl == 0x11:
            """
                system control
            """
            robot_addr = self.request_struct.DATA[0]
            system_action = self.request_struct.DATA[1]
            place_reserved = self.request_struct.DATA[2:]
            if system_action == 0:
                logger.info('Do not do anyting!')

            elif system_action == 1:
                print('SysReset')
                logger.info('SysReset!')
                if robot_addr == 0:
                    # robot_0.sys_reset()
                    print('===robot0 sysreset===')
                    t11 = threading.Thread(name="t11", target=sys_reset, args=('robot_0',0,siemens_1500, glock))
                    t11.start()

                    system_action_ack = self.request_struct.returnBytesList(0x91, [robot_addr])
                    self.response = system_action_ack  

                elif robot_addr == 1: 
                    print('==robot1 sysreset==')      
                    # robot_1.sys_reset()
                    t12 = threading.Thread(name="t12", target=sys_reset, args=('robot_1',1,siemens_1500, glock))
                    t12.start()

                    system_action_ack = self.request_struct.returnBytesList(0x91, [robot_addr])
                    self.response = system_action_ack  

            elif system_action == 2:
                logger.info('Return back on the same way!')
                # return_back = ReturnBack()
                # return_back.start()

            elif system_action == 3:
                logger.info('Back to the origin!')

            elif system_action == 4:
                logger.info('Continue execute!')

            elif system_action == 5:
                logger.info('--Reset---Wipe data!-----')
                if robot_addr == 0:
                    # robot_0.sys_reset()
                    # t11 = threading.Thread(name="t11", target=sys_reset, args=('robot_0',0,siemens_1500, glock))
                    # t11.start()
                    # time.sleep(0.2)
                    # bool_list = int2bitarray(gloVar.robot_0_system_reset_done, 8)
                    # logger.info(bool_list)
                    # if bool_list[4] == True:
                    logger.info("robot_0 system reset done")
                    system_action_ack = self.request_struct.returnBytesList(0x91, [robot_addr])
                    self.response = system_action_ack  

                elif robot_addr == 1:       
                    # robot_1.sys_reset()
                    # t12 = threading.Thread(name="t12", target=sys_reset, args=('robot_1',1,siemens_1500, glock))
                    # t12.start()
                    # time.sleep(0.2)

                    # bool_list = int2bitarray(gloVar.robot_1_system_reset_done, 8)
                    # logger.info(bool_list)

                    # if bool_list[4] == True:
                    system_action_ack = self.request_struct.returnBytesList(0x91, [robot_addr])
                    self.response = system_action_ack  

            elif system_action == 6:
                logger.info('Wipte battery quantity!')

            elif system_action == 7:
                logger.info('Left car in!')

                
            elif system_action == 8:
                logger.info('Left car out!')
             
                
            elif system_action == 9:
                logger.info('Right car in!')


            elif system_action == 10:
                logger.info('Right car out!')

        elif ctl == 0x12:
            """
                car model
            """
            robot_addr = self.request_struct.DATA[0]
            car_model = self.request_struct.DATA[1]
            place_reserved = self.request_struct.DATA[2:]

            if robot_addr == 0:
                # robot_0.select_car_model()
                t1 = threading.Thread(name="t1", target=select_car_model, args=('robot_0',0,siemens_1500, glock))
                t1.start()
            elif robot_addr == 1:       
                # robot_1.select_car_model()
                t2 = threading.Thread(name="t2", target=select_car_model, args=('robot_1',1,siemens_1500, glock))
                t2.start()

            logger.info('select_car_model_ack')
            select_car_model_ack = self.request_struct.returnBytesList(0x92, [robot_addr])
            self.response = select_car_model_ack 

        elif ctl == 0x20:
            """
                battery input/output
            """            
            robot_addr = self.request_struct.DATA[0]
            start_stop = self.request_struct.DATA[1]
            action_cmd = self.request_struct.DATA[2]            
            row_positon = self.request_struct.DATA[3]            
            column_position = self.request_struct.DATA[4]            
            battery_position_seq = self.request_struct.DATA[5]        
            place_holder = self.request_struct.DATA[6]  

            robot_no_str = 'robot_' + str(robot_addr)
            src_position = translate_row_col_to_position(row_positon, column_position)
            
            if start_stop == 0x55:
                # 启动
                if action_cmd == 0x01:
                    # 入库
                    if robot_addr == 0:
                        # robot_0.battery_input(src_position)
                        t3 = threading.Thread(name="t3", target=battery_input, args=('robot_0',0,siemens_1500, src_position, glock))
                        t3.start()
                    elif robot_addr == 1:
                        # robot_1.battery_input(src_position)
                        t4 = threading.Thread(name="t4", target=battery_input, args=('robot_1',1,siemens_1500, src_position, glock))
                        t4.start()
                elif action_cmd == 0x00:
                    # 出库
                    if robot_addr == 0:
                        # robot_0.battery_output(src_position)
                        t5 = threading.Thread(name="t5", target=battery_output, args=('robot_0',0,siemens_1500, src_position, glock))
                        t5.start()
                    elif robot_addr == 1:
                        # robot_1.battery_output(src_position)
                        t6 = threading.Thread(name="t6", target=battery_output, args=('robot_1',1,siemens_1500, src_position, glock))
                        t6.start()
            
            logger.info('in_out_ack')
            in_out_ack = self.request_struct.returnBytesList(0xA0, [robot_addr])
            self.response = in_out_ack  

        elif ctl == 0x21:
            """
                battery move
            """              
            robot_addr = self.request_struct.DATA[0]
            start_stop = self.request_struct.DATA[1]
            src_row = self.request_struct.DATA[2]            
            src_col = self.request_struct.DATA[3]            
            dst_row = self.request_struct.DATA[4]            
            dst_col = self.request_struct.DATA[5]                      
            emergency = self.request_struct.DATA[6]  
            place_holder_2 = self.request_struct.DATA[7] 

            src_position = translate_row_col_to_position(src_row, src_col)
            dst_position = translate_row_col_to_position(dst_row, dst_col)
  

            robot_no_str = 'robot_' + str(robot_addr)

            if start_stop == 0x55:
                # 启动
                if robot_addr == 0:
                    # robot_0.battery_move(src_position, dst_position)
                    t7 = threading.Thread(name="t7", target=battery_move, args=('robot_0',0,siemens_1500, src_position, dst_position, emergency, glock))
                    t7.start()
                elif robot_addr == 1:
                    # robot_1.battery_move(src_position, dst_position)
                    t8 = threading.Thread(name="t8", target=battery_move, args=('robot_1',1,siemens_1500, src_position, dst_position, emergency, glock))
                    t8.start()
            
            logger.info('battery_move_ack')
            battery_move_ack = self.request_struct.returnBytesList(0xA1, [robot_addr])
            self.response = battery_move_ack  

        elif ctl == 0x22:
            """
                battery input/output redo
            """         
            robot_addr = self.request_struct.DATA[0]
            start_stop = self.request_struct.DATA[1]
            action_cmd = self.request_struct.DATA[2]            
            row_positon = self.request_struct.DATA[3]            
            column_position = self.request_struct.DATA[4]            
            battery_position_seq = self.request_struct.DATA[5]            
            place_holder = self.request_struct.DATA[6]  
            
            dst_position = translate_row_col_to_position(row_positon, column_position)

            # 半自动处理，全自动不处理
            # right_car_position, left_car_position = divmod(battery_position_seq, 16)
            # 商，余数 divmod(49,16) = 3, 1

            if start_stop == 0x55:
                # 启动
                if action_cmd == 0x01:
                    # 再次入库
                    # 再入库只有目标位置
                    if robot_addr == 0:
                        # robot_0.redo_battery_input(dst_position)
                        t9 = threading.Thread(name="t9", target=redo_battery_input, args=('robot_0',0,siemens_1500, dst_position, glock))
                        t9.start()
                    elif robot_addr == 1:
                        # robot_1.redo_battery_input(dst_position)
                        t10 = threading.Thread(name="t10", target=redo_battery_input, args=('robot_1',1,siemens_1500,  dst_position, glock))
                        t10.start()

                elif action_cmd == 0x00:
                    # 再次出库
                    pass
            logger.info('redo_in_out_ack')
            robot_no_str = 'robot_' + str(robot_addr)
            redo_in_out_ack = self.request_struct.returnBytesList(0xA2, [robot_addr])
            self.response = redo_in_out_ack 

        else:
            self.response = struct.pack('B', 255)
            # 'unknown!'

            # logger.info('----gloVar.robot_0_system_status_global-----')
            # logger.info(gloVar.robot_0_system_status_global)
            # logger.info(gloVar.robot_1_system_status_global)

    def handle(self):  #所有请求的交互都是在handle里执行的,
        global isNew
        global stringSendToRobot

        while True:
            try:
                self.data = self.request.recv(BUFSIZE).strip()
                # logger.info("{} wrote:".format(self.client_address[0]))
                # logger.info(self.data)

                self.data_length = len(self.data)
                if len(self.data) < 5:
                    break

                # data from zhankong
                elif len(self.data) > 15 and len(self.data) < 100:
                    # logger.info('total length is:', self.data_length)
                    self.DATA_length = self.data_length - 16
                    # logger.info('DATA_length is:', self.DATA_length)

                    if self.DATA_length > 0:
                        data_fmt = '1B2B6B1B1B1B2B' + str(self.DATA_length) + 'B1B1B'
                        # logger.info('data_fmt is:', data_fmt)
                        self.msg_list = struct.unpack(data_fmt, self.data)
                        self.work_dispatch()
                    else:
                        no_data_fmt = '1B2B6B1B1B1B2B1B1B'
                        # logger.info('fmt size is:', struct.calcsize(no_data_fmt))
                        self.msg_list = struct.unpack(no_data_fmt, self.data)
                        self.work_dispatch()

                    if self.data == b'exit':
                        logger.info('ready to exit!')
                        break

                    # self.request.sendall(self.response)
                    self.wfile.write(self.response)

                elif len(self.data) == 200:
                    print('\n' * 5)
                    print('****' * 5)
                    print('get data from camera!')
                    isNew = True
                    print('======set isNew=======')
                    dataProcess(self.data)

                elif 'camera0' in self.data.strip()[:7].decode("utf-8"):
                    # logger.info('\n' * 5)
                    # logger.info('get data from camera1!')

                    scan_trigger_front = gloVar.robot_0_scan_trigger_front
                    scan_trigger_after = gloVar.robot_0_scan_trigger_after
                    camera_3_invalid = gloVar.robot_0_camera_3_invalid  
                    # 触发且无多次无效
                    scan_trigger_front_again = gloVar.robot_0_scan_trigger_front_again and not camera_3_invalid
                    scan_trigger_after_again = gloVar.robot_0_scan_trigger_after_again  and not camera_3_invalid
                    # scanner position
                    if scan_trigger_front:
                        gloVar.robot_0_scanner_positon = 0
                    if scan_trigger_after:
                        gloVar.robot_0_scanner_positon = 1

                    if scan_trigger_front or scan_trigger_after or scan_trigger_front_again or scan_trigger_after_again:
                        self.request.sendall(b'1')
                    else:
                        self.request.sendall(b'0')
                
                elif 'camera1' in self.data.strip()[:7].decode("utf-8"):
                    # logger.info('\n' * 5)
                    # logger.info('get data from camera2!')

                    scan_trigger_front = gloVar.robot_1_scan_trigger_front
                    scan_trigger_after = gloVar.robot_1_scan_trigger_after
                    camera_3_invalid = gloVar.robot_1_camera_3_invalid 

                    scan_trigger_front_again = gloVar.robot_1_scan_trigger_front_again and not camera_3_invalid
                    scan_trigger_after_again = gloVar.robot_1_scan_trigger_after_again and not camera_3_invalid     
                    # scanner position
                    if scan_trigger_front:
                        gloVar.robot_1_scanner_positon = 0
                    if scan_trigger_after:
                        gloVar.robot_1_scanner_positon = 1
                    if scan_trigger_front or scan_trigger_after or scan_trigger_front_again or scan_trigger_after_again:
                        self.request.sendall(b'1')
                    else:
                        self.request.sendall(b'0')  

                else:
                    logger.info('invalid string!')
                    # break

            except ConnectionResetError as e:
                print("err ", e)
                break

if __name__ == "__main__":

    global isNew 
    global stringSendToRobot 

    isNew = False
    stringSendToRobot = b'0,0,0,0,0,0,0,0'

    HOST, PORT = "192.168.0.110", 8000 #windows


    # host = "192.168.1.100"      #主机名，可以是ip,像localhost的主机名,或""
    # # host = ""      #主机名，可以是ip,像localhost的主机名,或""
    # port = 9999    #端口
    # addr = (host, port)

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

        siemens_1500 = gloVar.siemens_1500
        


        # server = socketserver.ThreadingTCPServer((HOST, PORT), MyStreamRequestHandler)   #线程
        # server.request_queue_size = 50
        # server.serve_forever()
    except KeyboardInterrupt as e:
        print(e)
        #print '^C received, shutting down server'
        # server.socket.close()