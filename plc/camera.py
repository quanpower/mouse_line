import threading
import time
import datetime
import struct
from utils import int2bitarray

from global_list import gloVar

import logging
logger = logging.getLogger(__name__)


def dont_do_anything():
    pass


def robot_action(siemens_1500, positionByte, position, enableByte, enableBit, enable, glock):
    logger.info('---robot action----start-----')
    print('---robot action----start-----')
    print(datetime.datetime.now())
    with glock:
        # siemens_1500.write_byte_to_plc(38, positionByte, position)
        time.sleep(0.1)

        # siemens_1500.write_bool_to_plc(38, enableByte, enableBit, enable)
    logger.info(position)
    logger.info('---robot action---end-------')
    print('---robot action---end-------')


def shift_action(siemens_1500, shiftxByte, shiftxValue,shiftyByte, shiftyValue,shiftzByte, shiftzValue,enableByte,enableBit,enableValue, glock):
    logger.info('---shift action----start-----')
    print('---shift action----start-----')
    print(datetime.datetime.now())
    print(shiftxValue)
    print(enableByte)
    print(enableBit)
    print(enableValue)

    with glock:
        siemens_1500.write_real_to_plc(38, shiftxByte, shiftxValue)
        siemens_1500.write_real_to_plc(38, shiftyByte, shiftyValue)
        siemens_1500.write_real_to_plc(38, shiftzByte, shiftzValue)
        siemens_1500.write_bool_to_plc(38, enableByte, enableBit, enableValue)
    logger.info('---shift action---end-------')
    print('---shift action---end-------')


def trigger_warehouse_camara(client_addr):
    print('===trigger_warehouse_camara_cmd===')
    trigger_warehouse_camara_bytes = (b'T1\r')
    print('trigger_warehouse_camara_bytes is:')
    print(trigger_warehouse_camara_bytes)

    client_socket = gloVar.sockets[client_addr]
    
    print(client_addr)
    print(client_socket)
    if client_addr:
        client_socket.sendall(trigger_warehouse_camara_bytes)
        print('===trigger_warehouse_camara_cmd sended!===')


def trigger_assembly_line_camara(client_addr, triggerCtl):
    print('===trigger_assembly_line_camara_cmd===')
    # trigger_assembly_line_camara_bytes = struct.pack('>3B2H3B', 0xF1, 0xF2, 0x06, 0x02, 0x00, 0x08, 0xF3, 0xF4)
    if triggerCtl == 'A101':
        trigger_assembly_line_camara_bytes = (b'A101\r')
    elif triggerCtl == 'B101':
        trigger_assembly_line_camara_bytes = (b'B101\r')
    elif triggerCtl == 'A201':
        trigger_assembly_line_camara_bytes = (b'A201\r')
    elif triggerCtl == 'A202':
        trigger_assembly_line_camara_bytes = (b'A202\r')
    elif triggerCtl == 'B201':
        trigger_assembly_line_camara_bytes = (b'B201\r')
    elif triggerCtl == 'B202':
        trigger_assembly_line_camara_bytes = (b'B202\r')        
    elif triggerCtl == 'B301':
        trigger_assembly_line_camara_bytes = (b'B301\r')        
    elif triggerCtl == 'B302':
        trigger_assembly_line_camara_bytes = (b'B302\r')        
    elif triggerCtl == 'A401':
        trigger_assembly_line_camara_bytes = (b'A401\r')
    elif triggerCtl == 'B401':
        trigger_assembly_line_camara_bytes = (b'B401\r')
    else:
        trigger_assembly_line_camara_bytes = (b'error')

    if trigger_assembly_line_camara_bytes != (b'error'):
        print('trigger_assembly_line_camara_bytes is:')
        print(trigger_assembly_line_camara_bytes)

        client_socket = gloVar.sockets[client_addr]
        
        print(client_addr)
        print(client_socket)
        if client_addr:
            client_socket.sendall(trigger_assembly_line_camara_bytes)
            print('===trigger_assembly_line_camara_cmd sended!===')


def camera_trigger():
    while True:
        camera1_ip = '172.16.6.220'
        camera2_ip = '172.16.6.221'

        camera_triggers = gloVar.camera_triggers
        # print('=====camera_triggers====')
        # print(camera_triggers)
        
        # 人工上料台到立库->入库触发
        if camera_triggers[0]:
            thread_trigger = threading.Thread(name="thread_trigger", target=trigger_warehouse_camara, args=(camera1_ip,))
            thread_trigger.start()
        if camera_triggers[1]:
            if gloVar.category=='A':
                triggerCtl = 'A101'
            else:
                triggerCtl = 'B101'
            thread_trigger = threading.Thread(name="thread_trigger", target=trigger_assembly_line_camara, args=(camera2_ip, triggerCtl))
            thread_trigger.start() 
        if camera_triggers[2]:
            if gloVar.category=='A':
                triggerCtl = 'A201'
            else:
                triggerCtl = 'B201'
            thread_trigger = threading.Thread(name="thread_trigger", target=trigger_assembly_line_camara, args=(camera2_ip, triggerCtl))
            thread_trigger.start() 
        if camera_triggers[3]:
            if gloVar.category=='A':
                triggerCtl = 'A202'
            else:
                triggerCtl = 'B202'
            thread_trigger = threading.Thread(name="thread_trigger", target=trigger_assembly_line_camara, args=(camera2_ip, triggerCtl))
            thread_trigger.start() 
        if camera_triggers[4]:
            if gloVar.category=='A':
                triggerCtl = 'A301'
            else:
                triggerCtl = 'B301'
            thread_trigger = threading.Thread(name="thread_trigger", target=trigger_assembly_line_camara, args=(camera2_ip, triggerCtl))
            thread_trigger.start() 
        if camera_triggers[5]:
            if gloVar.category=='A':
                triggerCtl = 'A302'
            else:
                triggerCtl = 'B302'
            thread_trigger = threading.Thread(name="thread_trigger", target=trigger_assembly_line_camara, args=(camera2_ip, triggerCtl))
            thread_trigger.start()      
        if camera_triggers[6]:
            if gloVar.category=='A':
                triggerCtl = 'A401'
            else:
                triggerCtl = 'B401'
            thread_trigger = threading.Thread(name="thread_trigger", target=trigger_assembly_line_camara, args=(camera2_ip, triggerCtl))
            thread_trigger.start()   

        time.sleep(0.5)                                                      