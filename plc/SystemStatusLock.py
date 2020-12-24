import threading
import time
import struct
from plc_addr import robots_addr
from utils import int2bitarray
import binascii
import random
import logging

from camera import trigger_assembly_line_camara, trigger_warehouse_camara, shift_action

logger = logging.getLogger(__name__)

# 导入全局变量
from global_list import gloVar


def query_system_status(glock):
    while True:    
        try:
            siemens_1500 =  gloVar.siemens_1500
            with glock:
                try:
                    # print('=====robot_0======')
                    
                    warehouse_senser_status = siemens_1500.query_block_from_plc(40,0,8)
                    wss =struct.unpack('<2I', warehouse_senser_status)
                    status_a = wss[0]
                    status_b = wss[1]
                    bitArrayA = int2bitarray(status_a,32)
                    bitArrayB = int2bitarray(status_b, 32)

                    camera_trigger = siemens_1500.query_block_from_plc(38,0,1)
                    ct =struct.unpack('>B', camera_trigger)
                    # print('===camera_trigger===')
                    camera_triggers = int2bitarray(ct[0], 8)
                    # print(camera_triggers)
                    ready_ok = camera_triggers[7]

                    robot_status = siemens_1500.query_block_from_plc(38,16,28)
                    rs =struct.unpack('>14H', robot_status)
                    # print(rs)
                    gripper = rs[0]
                    z2 = rs[1]
                    z3_1 = rs[2]
                    z3_2 = rs[3]
                    z4_1 = rs[4]
                    z4_2 = rs[5]
                    z5 = rs[6]
                    z6 = rs[7]
                    r2_plate = rs[8]
                    r3_plate_1 = rs[9]
                    r3_plate_2 = rs[10]
                    r4_plate_1 = rs[11]
                    r4_plate_2 = rs[12]
                    r7_plate = rs[13]


                    logger.info('=====warehouse_senser_status======')
                    logger.info(wss)
                    logger.info(rs)
                    # print('=====warehouse_senser_status======')
                    # print(bitArrayA)
                    # print(bitArrayB)
                    logger.info(bitArrayA)
                    logger.info(bitArrayB)

                    if wss:
                        gloVar.warehouse_senser_status = wss
                    if camera_triggers:
                        gloVar.camera_triggers = camera_triggers
                        gloVar.ready_ok = ready_ok
                    if rs:
                        gloVar.robot_status = rs
                    gloVar.bitArrayA = bitArrayA
                    gloVar.bitArrayB = bitArrayB
                    
                except Exception as e:
                    print(e)
                    logger.error(e)

            time.sleep(0.2)
            # time.sleep(0.2)

        except  Exception as e:
            logger.error(e) 
