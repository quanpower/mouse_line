import threading
import time
import datetime
import struct
from utils import int2bitarray
import requests
from global_list import gloVar
import json
import logging
from utils import generate_plate_info_json, get_material_dict

logger = logging.getLogger(__name__)


def dont_do_anything():
    pass

material_dict = get_material_dict()

def get_material_code(position):
    for key,value in material_dict.items():
        if str(position) in value:
            return key


def in_action(siemens_1500, positionByte, position, enableByte, enableBit, enable, goods, glock):
    logger.info('---in action----start-----')
    print('---in action----start-----')
    print(datetime.datetime.now())
    with glock:
        siemens_1500.write_int_to_plc(38, positionByte, position)
        time.sleep(0.1)
        siemens_1500.write_bool_to_plc(38, enableByte, enableBit, enable)
    logger.info(position)
    logger.info('---in action---end-------')
    print('---in action---end-------')

    while True:
        if gloVar.warehouse_put_ok:
            # 放件完成，更新入库

            material_code = get_material_code(position)
            print(material_code)

            if goods == 6:
                # box
                material_list = generate_plate_info_json(1,7,material_code)
            elif goods == 3:
                # bottom
                material_list = generate_plate_info_json(1,10,material_code)
            elif goods == 2:
                # middle
                material_list = generate_plate_info_json(1,10,material_code)
            elif goods == 1:
                # up
                material_list = generate_plate_info_json(1,10,material_code)
            elif goods == 4:
                # battery
                material_list = generate_plate_info_json(1,55,material_code)
            elif goods == 5:
                # battery_lid
                material_list = generate_plate_info_json(1,53,material_code)

            url = 'http://localhost:8088/v1/api/wms/warehouse/bin/' + str(position)
            param = {'isEmpty': 0,
            'materialList': material_list
            }

            payload = json.dumps(param)
            response_put = requests.put(url, data=payload)
            break
        
        i += 1
        print(i)
        # 跳出while,结束入库
        if i >= 60:
            return
        time.sleep(1)        



def out_action(siemens_1500, positionByte,noByte,quantityByte, enableByte, enableBit, enable, out_list, glock):
    logger.info('---out action----start-----')
    print('---out action----start-----')
    print(out_list)
    for out in out_list:
        i = 0
        while 1: 
            print(datetime.datetime.now())
            position = out['position']
            no = out['no']
            quantity = out['quantity']

            if gloVar.ready_ok:
                print('=====output no=====')
                print(position)
                with glock:
                    siemens_1500.write_int_to_plc(38, positionByte, position)
                    time.sleep(0.1)
                    siemens_1500.write_int_to_plc(38, noByte, no)
                    time.sleep(0.1)
                    siemens_1500.write_int_to_plc(38, quantityByte, quantity)
                    time.sleep(0.1)
                    siemens_1500.write_bool_to_plc(38, enableByte, enableBit, enable)
                    print(positionByte)
                    print(enableByte)
                    print(enableBit)
                    print(enable)

                time.sleep(3)

                # 出库使能复位
                with glock:
                    siemens_1500.write_bool_to_plc(38, enableByte, enableBit, 0)
                logger.info(position)
                break

            i += 1
            print(i)

            # 跳出while,结束出库
            if i >= 600:
                siemens_1500.write_bool_to_plc(38, enableByte, enableBit, 0)
                return
            time.sleep(1)

    logger.info('---out action---end-------')
    print('---out action---end-------')


def load_action(siemens_1500, positionByte,noByte,quantityByte, enableByte, enableBit, enable, out_list, glock):
    logger.info('---out action----start-----')
    print('---out action----start-----')
    print(out_list)
    for out in out_list:
        i = 0
        while 1: 
            print(datetime.datetime.now())
            position = out['position']
            no = out['no']
            quantity = out['quantity']

            if gloVar.ready_ok:
                print('=====output no=====')
                print(position)
                with glock:
                    siemens_1500.write_int_to_plc(38, positionByte, position)
                    time.sleep(0.1)
                    siemens_1500.write_int_to_plc(38, noByte, no)
                    time.sleep(0.1)
                    siemens_1500.write_int_to_plc(38, quantityByte, quantity)
                    time.sleep(0.1)
                    siemens_1500.write_bool_to_plc(38, enableByte, enableBit, enable)
                    print(positionByte)
                    print(enableByte)
                    print(enableBit)
                    print(enable)

                time.sleep(3)

                # 出库使能复位
                with glock:
                    siemens_1500.write_bool_to_plc(38, enableByte, enableBit, 0)
                logger.info(position)
                break

            if gloVar.warehouse_get_ok:
                # 取件完成，更新出库,
                material_list = generate_plate_info_json(1,10,'null')

                url = 'http://localhost:8088/v1/api/wms/warehouse/bin/' + str(position)
                param = {'isEmpty': 1,
                'materialList': material_list
                }

                payload = json.dumps(param)
                response_put = requests.put(url, data=payload)
                break

            i += 1
            print(i)
            # 跳出while,结束出库
            if i >= 600:
                siemens_1500.write_bool_to_plc(38, enableByte, enableBit, 0)
                return
            time.sleep(1)

    logger.info('---out action---end-------')
    print('---out action---end-------')


def unload_action(siemens_1500, positionByte, position, enableByte, enableBit, enable, glock):
    logger.info('---in action----start-----')
    print('---in action----start-----')
    print(datetime.datetime.now())
    with glock:
        siemens_1500.write_int_to_plc(38, positionByte, position)
        time.sleep(0.1)
        siemens_1500.write_bool_to_plc(38, enableByte, enableBit, enable)
    logger.info(position)
    logger.info('---in action---end-------')
    print('---in action---end-------')

    while True:
        if gloVar.warehouse_put_ok:
            # 放件完成，更新入库

            material_code = get_material_code(position)
            print(material_code)
            print(gloVar.robot_status[8])
            # 更新数量
            material_list = generate_plate_info_json(1,10,material_code)

            url = 'http://localhost:8088/v1/api/wms/warehouse/bin/' + str(position)
            param = {'isEmpty': 0,
            'materialList': material_list
            }

            payload = json.dumps(param)
            response_put = requests.put(url, data=payload)
            break
        
        i += 1
        print(i)
        # 跳出while,结束入库
        if i >= 60:
            return
        time.sleep(1)        



