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
                    ###########################################--------DB40----------###########################################
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

                    # 立库取件完成
                    warehouse_get_ok = rpgds_array_0[4]
                    # 立库放件完成
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
                    
                    # 从线边库取件完成
                    line_get_ok_list = [z2_get_ok, z3_get_ok, z4_get_ok, z5_get_ok, z6_get_ok, z7_get_ok]
                    # 往线边库放件完成
                    line_put_ok_list = [z2_put_ok, z3_put_ok, z4_put_ok, z5_put_ok, z6_put_ok, z7_put_ok]
                    # 此单完成信号
                    work_done = rpgds_array_2[2]
                    # 预生产信号
                    pre_order_ok = rpgds_array_2[3]

                    # 生产过程种取件完成，更新线边库
                    producing_get_ok = siemens_1500.query_block_from_plc(40,11,1)
                    producing_get_ok_list = struct.unpack('>B', producing_get_ok)
                    # print(producing_get_ok_list)
                    producing_get_ok_array = int2bitarray(producing_get_ok_list[0], 8)
                    z2_bottom_get_ok = producing_get_ok_array[0]
                    z3_middle_get_ok = producing_get_ok_array[1]
                    z3_top_get_ok = producing_get_ok_array[2]
                    z4_battery_get_ok = producing_get_ok_array[3]           
                    z4_black_lid_get_ok = producing_get_ok_array[4]
                    z4_white_lid_get_ok = producing_get_ok_array[5]
                    z7_box_get_ok = producing_get_ok_array[6]

                    producing_bool_get_ok_list =[z2_bottom_get_ok, z3_middle_get_ok, z3_top_get_ok, z4_battery_get_ok, z4_black_lid_get_ok, z4_white_lid_get_ok, z7_box_get_ok]


                    #######################################--------DB38----------###########################################
                    ###########-----------相机触发-------------##############
                    camera_trigger = siemens_1500.query_block_from_plc(38,0,1)
                    ct =struct.unpack('>B', camera_trigger)
                    # print('===camera_trigger===')
                    camera_triggers = int2bitarray(ct[0], 8)
                    # print(camera_triggers)

                    # 堆垛机准备完成,准备从立库取件
                    ready_ok = camera_triggers[7]


                    # 托盘检测
                    plate_check = siemens_1500.query_block_from_plc(38,5,1)
                    pc =struct.unpack('>B', plate_check)
                    # print('===plate_check===')
                    plate_check_list = int2bitarray(pc[0], 8)
                    # print(plate_check_list)

                    # -->线边库，上料
                    robot_status = siemens_1500.query_block_from_plc(38,16,28)
                    rs =struct.unpack('>14H', robot_status)
                    # print(rs)
                    gripper = rs[0]
                    
                    # 各工位检测有无托盘 
                    z2 = rs[1]
                    z3_1 = rs[2]
                    z3_2 = rs[3]
                    z4_1 = rs[4]
                    z4_2 = rs[5]
                    z5 = rs[6]
                    z6 = rs[7]

                    # 各工位托盘内器件数量
                    r2_bottom_plate = rs[8]
                    r3_middle_plate = rs[9]
                    r3_top_plate = rs[10]
                    r4_battery_plate = rs[11]
                    r4_battery_lid_plate = rs[12]
                    r7_box_plate = rs[13]
                    producing_quanlity_list = [r2_bottom_plate, r3_middle_plate, r3_top_plate, r4_battery_plate, r4_battery_lid_plate, r7_box_plate]
                    
                    #####################################----------------更新全局变量----------------############################################
                    gloVar.warehouse_senser_status = wss
                    gloVar.camera_triggers = camera_triggers
                    gloVar.robot_status = rs
                    
                    # 立库传感器判断
                    gloVar.wssArray = wssArray
                    
                    # 新订单准备完成
                    gloVar.pre_order_ok = pre_order_ok

                    # 堆垛机准备完成
                    gloVar.ready_ok = ready_ok
                    
                    # 上下料取放件完成
                    gloVar.warehouse_get_ok = warehouse_get_ok
                    gloVar.warehouse_put_ok = warehouse_put_ok

                    gloVar.line_get_ok_list = line_get_ok_list
                    gloVar.line_put_ok_list = line_put_ok_list
                    gloVar.plate_check_list = plate_check_list

                    # 生产取料完成
                    gloVar.producing_bool_get_ok_list = producing_bool_get_ok_list
                    # 生产线工位上托盘内器件数量
                    gloVar.producing_quanlity_list = producing_quanlity_list
                    
                    # 订单完成
                    gloVar.work_done = work_done
                    # 不生产时，把状态设为完成
                    if work_done:
                        gloVar.state = 3
                        
                    # logger.info('\n'*3)
                    # logger.info('=====warehouse_senser_status======')
                    # logger.info('====wssArray===')
                    # logger.info(wssArray)
                    # logger.info('===warehouse_put_ok===')
                    # logger.info(warehouse_put_ok)
                    # logger.info('====warehouse_get_ok====')
                    # logger.info(warehouse_get_ok)
                    # logger.info('===line_get_ok_list====')
                    # logger.info(line_get_ok_list)
                    # logger.info('====line_put_ok_list=====')
                    # logger.info(line_put_ok_list)
                    # logger.info('======plate_check_list=====')
                    # logger.info(plate_check_list)
                    # logger.info('====work_done======')
                    # logger.info(work_done)
                    # logger.info('====ready_ok======')
                    # logger.info(ready_ok)
                    # logger.info('====pre_order_ok======')
                    # logger.info(pre_order_ok) 

                except Exception as e:
                    print(e)
                    logger.error(e)

            time.sleep(0.5)
            # time.sleep(0.2)

        except  Exception as e:
            logger.error(e) 
