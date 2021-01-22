import threading
import time
import datetime
import struct
from utils import int2bitarray
import requests
from global_list import gloVar
import json
import logging
from utils import generate_plate_info_json, get_material_dict, \
    generate_material_list_json, generate_null_material_list_json, generate_linestorage_no, \
        generate_unload_material_list_json

logger = logging.getLogger(__name__)



mes_warehouse_snapshot_url ="http://172.16.1.62/aim-mes/open-api/wms/snapshot/v1/list"
mes_line_storage_snapshot_url ="http://172.16.1.62/aim-mes/open-api/wms-line/snapshot/v1/list"

warehouse_snapshot_url = "http://localhost:8088/v1/api/wms/warehouse/snapshot/list"
line_storage_snapshot_url = "http://localhost:8088/v1/api/wms/line_storage/snapshot/list"

warehouse_bin_url = "http://localhost:8088/v1/api/wms/warehouse/bin/"
line_storage_bin_url = "http://localhost:8088/v1/api/wms/line_storage/bin/"

warehouse_version_url = "http://localhost:8088/v1/api/wms/warehouse/version"
line_storage_version_url = "http://localhost:8088/v1/api/wms/line_storage/version"

def dont_do_anything():
    pass

material_dict = get_material_dict()

def get_material_code(position):
    for key,value in material_dict.items():
        if str(position) in value:
            return key


def post_mes_warehouse():
    # get 最新立库信息
    warehouse_snapshot = requests.get(warehouse_snapshot_url)
    warehouse_snapshot_json = warehouse_snapshot.json()
    warehouse_snapshot_list = warehouse_snapshot_json['data']
    print('====warehouse_snapshot_list.json()====')
    print(warehouse_snapshot_list.json())
    # post到MES
    mes_warehouse_snapshot_post = requests.post(mes_warehouse_snapshot_url,data=warehouse_snapshot_list)
    #response = r.json()
    print ('=====mes_warehouse_snapshot_post.text====')
    print (mes_warehouse_snapshot_post.text)


def post_mes_line_storage():
    # get 最新线边库
    line_storage_snapshot = requests.get(line_storage_snapshot_url)
    line_storage_snapshot_json = line_storage_snapshot.json()
    line_storage_snapshot_list = line_storage_snapshot_json['data']                
    print('=====line_storage_snapshot_list.json()=====')
    print(line_storage_snapshot_list.json())
    # post MES
    mes_line_storage_snapshot_post = requests.post(mes_line_storage_snapshot_url,data=line_storage_snapshot_list)
    #response = r.json()
    print ('=====mes_line_storage_snapshot_post.text=====')                
    print (mes_line_storage_snapshot_post.text) 


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

    i = 0
    while True:
        if gloVar.warehouse_put_ok:
            # 放件完成，更新入库

            # material_code = get_material_code(position)
            # print(material_code)

            # if goods == 6:
            #     # box
            #     material_list = generate_plate_info_json(1,7,material_code)
            # elif goods == 3:
            #     # bottom
            #     material_list = generate_plate_info_json(1,10,material_code)
            # elif goods == 2:
            #     # middle
            #     material_list = generate_plate_info_json(1,10,material_code)
            # elif goods == 1:
            #     # up
            #     material_list = generate_plate_info_json(1,10,material_code)
            # elif goods == 4:
            #     # battery
            #     material_list = generate_plate_info_json(1,55,material_code)
            # elif goods == 5:
            #     # battery_lid
            #     material_list = generate_plate_info_json(1,53,material_code)

            material_list = generate_material_list_json(position)

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
        position = out['position']
        no = out['no']
        quantity = out['quantity']

        line_no = generate_linestorage_no(position)
        line_trigger = gloVar.line_put_ok_list[line_no-1]

        warehouse_url = warehouse_bin_url + str(position)
        line_storage_url = line_storage_bin_url + str(line_no)

        r = requests.get(warehouse_url)
        return_json = r.json()
        source_material_list = return_json['data']

        while 1: 
            print(datetime.datetime.now())

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
                # 取件完成，更新立库
                material_list = generate_null_material_list_json(position)
                param = {'isEmpty': 1,
                'materialList': material_list
                }
                payload = json.dumps(param)
                response_put = requests.put(warehouse_url, data=payload)
                print('=====response_put.json()====')
                print(response_put.json())
                
                post_mes_warehouse()

            if line_trigger:
                # 放件完成，更新线边库,
                material_list = generate_null_material_list_json(position)
                param = {'isEmpty': 0,
                'materialList': source_material_list,
                'source': position
                }
                payload = json.dumps(param)
                response_put = requests.put(line_storage_url, data=payload)
                print('=====response_put.json()====')
                print(response_put.json())

                post_mes_line_storage()             

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
    # with glock:
    #     siemens_1500.write_int_to_plc(38, positionByte, position)
    #     time.sleep(0.1)
    #     siemens_1500.write_bool_to_plc(38, enableByte, enableBit, enable)
    logger.info(position)
    logger.info('---in action---end-------')
    print('---in action---end-------')

    i = 0
    while True:

        line_trigger = gloVar.line_put_ok_list[line_no-1]

        warehouse_url = warehouse_bin_url + str(position)
        line_storage_url = line_storage_bin_url + str(line_no)

        r = requests.get(line_storage_url)
        return_json = r.json()
        source_material_list = return_json['data']

        if line_trigger:
            post_mes_line_storage()

        if gloVar.warehouse_put_ok:
            # 放件完成，更新入库
            material_code = get_material_code(position)
            print(material_code)
            print(gloVar.robot_status[8])
            # 更新数量
            material_list = generate_unload_material_list_json(1,10,material_code)

            url = 'http://localhost:8088/v1/api/wms/warehouse/bin/' + str(position)
            param = {'isEmpty': 0,
            'materialList': source_material_list
            }

            payload = json.dumps(param)
            response_put = requests.put(url, data=payload)

            post_mes_warehouse()

            break
        
        i += 1
        print(i)
        # 跳出while,结束入库
        if i >= 60:
            return
        time.sleep(1)        



