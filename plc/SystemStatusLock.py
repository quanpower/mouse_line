import threading
import time
import struct
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
                    # 立库52格位有无信号
                    warehouse_senser_status = siemens_1500.query_block_from_plc(40,0,8)
                    wss =struct.unpack('<2I', warehouse_senser_status)
                    status_a = wss[0]
                    status_b = wss[1]
                    bitArrayA = int2bitarray(status_a, 32)
                    bitArrayB = int2bitarray(status_b, 32)
                    bitArrayA.extend(bitArrayB)
                    wssArray = bitArrayA[0:52]

                    # 取件，放件完成
                    robot_put_get_done_status = siemens_1500.query_block_from_plc(40,8,3)
                    rpgds = struct.unpack('>3B', robot_put_get_done_status)
                    # print(rpgds)
                    rpgds_array_0 = int2bitarray(rpgds[0], 8)
                    rpgds_array_1 = int2bitarray(rpgds[1], 8)
                    rpgds_array_2 = int2bitarray(rpgds[2], 8)

                    warehouse_get_ok = rpgds_array_0[4]
                    warehouse_put_ok = rpgds_array_0[5]
                    z2_get_ok = rpgds_array_0[6]
                    z2_put_ok = rpgds_array_0[7]

                    z3_get_ok = rpgds_array_1[0]
                    z3_put_ok = rpgds_array_1[1]
                    z4_get_ok = rpgds_array_1[2]
                    z4_put_ok = rpgds_array_1[3]           
                    z5_get_ok = rpgds_array_1[4]
                    z5_put_ok = rpgds_array_1[5]
                    z6_get_ok = rpgds_array_1[6]
                    z6_put_ok = rpgds_array_1[7]  

                    z7_get_ok = rpgds_array_2[0]
                    z7_put_ok = rpgds_array_2[1]  

                    line_get_ok_list = [z2_get_ok, z3_get_ok, z4_get_ok, z5_get_ok, z6_get_ok, z7_get_ok]
                    line_put_ok_list = [z2_put_ok, z3_put_ok, z4_put_ok, z5_put_ok, z6_put_ok, z7_put_ok]

                    producing = rpgds_array_2[2]
                    
                    # 相机触发
                    camera_trigger = siemens_1500.query_block_from_plc(38,0,1)
                    ct =struct.unpack('>B', camera_trigger)
                    # print('===camera_trigger===')
                    camera_triggers = int2bitarray(ct[0], 8)
                    # print(camera_triggers)
                    # 准备完成
                    ready_ok = camera_triggers[7]

                    # 托盘检测
                    plate_check = siemens_1500.query_block_from_plc(38,5,1)
                    pc =struct.unpack('>B', plate_check)
                    # print('===plate_check===')
                    plate_check_list = int2bitarray(pc[0], 8)
                    # print(plate_check_list)

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
                    logger.info(wssArray)

                    # print('=====warehouse_senser_status======')
                    # print(bitArrayA)
                    # print(bitArrayB)
                    # print(wssArray)

                    if wss:
                        gloVar.warehouse_senser_status = wss
                    if camera_triggers:
                        gloVar.camera_triggers = camera_triggers
                        gloVar.ready_ok = ready_ok
                    if rs:
                        gloVar.robot_status = rs

                    gloVar.wssArray = wssArray

                    gloVar.warehouse_get_ok = warehouse_get_ok
                    gloVar.warehouse_put_ok = warehouse_put_ok

                    gloVar.line_get_ok_list = line_get_ok_list
                    gloVar.line_put_ok_list = line_put_ok_list
                    gloVar.plate_check_list = plate_check_list

                    # gloVar.z3_get_ok = z3_get_ok
                    # gloVar.z3_put_ok = z3_put_ok
                    # gloVar.z4_get_ok = z4_get_ok
                    # gloVar.z4_put_ok = z4_put_ok          
                    # gloVar.z5_get_ok = z5_get_ok
                    # gloVar.z5_put_ok = z5_put_ok
                    # gloVar.z6_get_ok = z6_get_ok
                    # gloVar.z6_put_ok = z6_put_ok  

                    # gloVar.z7_get_ok = z7_get_ok
                    # gloVar.z7_put_ok = z7_put_ok  

                    gloVar.producing = producing
                    
                except Exception as e:
                    print(e)
                    logger.error(e)

            time.sleep(0.2)
            # time.sleep(0.2)

        except  Exception as e:
            logger.error(e) 
