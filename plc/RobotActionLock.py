import threading
import time
import datetime
import struct
from utils import int2bitarray
import requests
from urllib import parse
from global_list import gloVar
import json
import logging
from utils import generate_plate_info_json, get_material_dict, \
    generate_material_list_json, generate_null_material_list_json, generate_linestorage_no, \
        generate_line_storage_info_null

logger = logging.getLogger(__name__)



mes_warehouse_snapshot_url ="http://172.16.1.62/aim-mes/open-api/wms/snapshot/v1/list"
mes_line_storage_snapshot_url ="http://172.16.1.62/aim-mes/open-api/wms-line/snapshot/v1/list"

warehouse_snapshot_url = "http://localhost:8088/v1/api/wms/warehouse/snapshot/list"
line_storage_snapshot_url = "http://localhost:8088/v1/api/wms/line_storage/snapshot/list"

warehouse_bin_url = "http://localhost:8088/v1/api/wms/warehouse/bin/"
line_storage_bin_url = "http://localhost:8088/v1/api/wms/line_storage/bin/"

warehouse_version_url = "http://localhost:8088/v1/api/wms/warehouse/version"
line_storage_version_url = "http://localhost:8088/v1/api/wms/line_storage/version"

head = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}

def dont_do_anything():
    pass

material_dict = get_material_dict()

def get_material_code(position):
    for key,value in material_dict.items():
        if str(position) in value:
            return key

# 写string到西门子PLC
def write_string_to_plc(s1500,string2plc,start):
    s = '00' + string2plc
    byarray=bytearray(s,encoding='utf-8')
    # print(byarray)
    for i, val in enumerate(byarray):
        index = start + i 
        # print ("序号：%s   值：%s" % (i + 1, val))
        s1500.write_area(0x84,38,index, struct.pack('B', val))

# 获取数据库materiallist源
def get_source_material_list(warehouse_url):
    r = requests.get(warehouse_url)
    return_json = r.json()
    source_material_list_str = return_json['data'][0]['materialList']

    # print('======source_material_list_str=====')
    # print(source_material_list_str)
    # logger.info('======source_material_list_str=====')
    # logger.info(source_material_list_str)

    return source_material_list_str


# # 从数据库materiallist源列表生成json列表
# def (source_material_list_str):
#     # print('===source_material_list_str===')
#     # print(source_material_list_str)
#     # print(type(source_material_list_str))
#     logger.info('===source_material_list_str===')
#     logger.info(source_material_list_str)

#     source_material_list_dict = json.loads(source_material_list_str)
#     source_material_list = []
#     for key,value in source_material_list_dict.items():
#         plate = {}
#         plate['materialPlace'] = key
#         plate['materialCode'] = value
#         source_material_list.append(plate)
    
#     return source_material_list


# 更新立库储位为空
def update_warehouse_null(warehouse_url, position):
    material_list = generate_null_material_list_json(position)
    param = {'isEmpty': 1,
        'materialList': material_list
    }
    payload = json.dumps(param)
    response_put = requests.put(warehouse_url, data=payload)
    logger.info('=====warehouse_url_response_put.json()====')
    logger.info(response_put.json()) 


# 创建新的立库outandin版本
def create_new_warehouse_version(action, positionCode, source_material_list):
    param = {'action': action,
        'positionCode': positionCode,
        'materialList': source_material_list
    }                
    payload = json.dumps(param)
    warehouse_version_post = requests.post(warehouse_version_url, data=payload)
    print('=====create_new_warehouse_version====')
    logger.info('=====create_new_warehouse_version====') 

    logger.info('=====warehouse_version_post.json()====')
    logger.info(warehouse_version_post.json())  
    print('=====warehouse_version_post.json()====')
    print(warehouse_version_post.json())      


# 创建新的线边库outandin版本
def create_new_line_storage_version(action, positionCode, source_material_list):
    param = {'action': action,
        'positionCode': positionCode,
        'materialList': source_material_list
    }                
    payload = json.dumps(param)
    line_storage_version_post = requests.post(line_storage_version_url, data=payload)
    logger.info('=====line_storage_version_post.json()====')
    logger.info(line_storage_version_post.json())  


# 更新线边库储位
def update_line_storage_bin(line_storage_url, position, source_material_list):
    logger.info('====line_storage_update_source_material_list===')
    logger.info(source_material_list)
    try:
        param = {'isEmpty': 0,
        'materialList': source_material_list,
        'source': position
        }
        payload = json.dumps(param)

        logger.info('====line_storage_update_payload===')
        logger.info(payload)

        response_put = requests.put(line_storage_url, data=payload)
        logger.info('=====line_storage_url_response_put.json()====')
        logger.info(response_put.json())                
    except Exception as e:
        logger.error('=====line_storage_update_error====')
        logger.error(e)    

# POST warehouse信息到MES
def post_mes_warehouse():
    try:
        # get 最新立库信息
        warehouse_snapshot = requests.get(warehouse_snapshot_url)
        warehouse_snapshot_json = warehouse_snapshot.json()
        warehouse_snapshot_list = warehouse_snapshot_json['data']
        requestdata = parse.urlencode(warehouse_snapshot_list)

        # post到MES,hearers
        mes_warehouse_snapshot_post = requests.post(mes_warehouse_snapshot_url,data=requestdata,headers=head)
        #response = r.json()
        print('=====mes_warehouse_snapshot_post.json()====')
        print(mes_warehouse_snapshot_post.json())
        logger.info('=====mes_warehouse_snapshot_post.json()====')
        logger.info(mes_warehouse_snapshot_post.json())
    except Exception as e:
        logger.error ('====post_mes_warehouse error=====') 
        logger.error (e) 

# POST line storage信息到MES
def post_mes_line_storage():
    try:
        # get 最新线边库
        line_storage_snapshot = requests.get(line_storage_snapshot_url)
        line_storage_snapshot_json = line_storage_snapshot.json()
        line_storage_snapshot_list = line_storage_snapshot_json['data']                
        requestdata = parse.urlencode(line_storage_snapshot_list)

        # post到MES,hearers
        mes_line_storage_snapshot_post = requests.post(mes_line_storage_snapshot_url,data=requestdata,headers=head)   
        print('=====mes_line_storage_snapshot_post.json()=====')                
        print(mes_line_storage_snapshot_post.json()) 
        logger.info('=====mes_line_storage_snapshot_post.json()=====')                
        logger.info(mes_line_storage_snapshot_post.json()) 
    except Exception as e:
        logger.error ('post_mes_line_storage error') 
        logger.error (e) 

# 入库动作流程
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
            # todo:
            material_list = generate_material_list_json(position, start)

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

# 出库动作流程
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

# 上料动作流程
def load_action(siemens_1500, positionByte,noByte,quantityByte, enableByte, enableBit, enable, out_list, seq, productCode, glock):
    logger.info('---load_action----start-----')
    print('---load_action----start-----')
    print(out_list)

    for out in out_list:
        i = 0
        position = out['position']
        no = out['no']
        quantity = out['quantity']

        line_no = generate_linestorage_no(position)

        warehouse_url = warehouse_bin_url + str(position)
        line_storage_url = line_storage_bin_url + str(line_no)
        logger.info(warehouse_url)
        logger.info(line_storage_url)

        # 获取托盘信息
        source_material_list = get_source_material_list(warehouse_url)

        # PLC指令写一次
        can_write_flag = True
        # 上料流程
        while 1: 
            # 一、当堆垛机准备OK时，发给PLC机器人移动指令：

            # logger.info('====gloVar.ready_ok====')
            # logger.info(gloVar.ready_ok)

            if gloVar.ready_ok:
                # logger.info('=====output no=====')
                # logger.info(position)
                # print(position)
                if can_write_flag:
                    with glock:
                        siemens_1500.write_int_to_plc(38, positionByte, position)
                        time.sleep(0.1)
                        siemens_1500.write_int_to_plc(38, noByte, no)
                        time.sleep(0.1)
                        siemens_1500.write_int_to_plc(38, quantityByte, quantity)
                        time.sleep(0.1)
                        siemens_1500.write_bool_to_plc(38, enableByte, enableBit, enable)
                        # 写入订单号，产品号
                        write_string_to_plc(siemens_1500, seq, 98 )
                        write_string_to_plc(siemens_1500, productCode, 354 )
                can_write_flag = False

            # 二、当立库取件完成时，更新立库储位

            # logger.info('====gloVar.warehouse_get_ok====')
            # logger.info(gloVar.warehouse_get_ok)

            if gloVar.warehouse_get_ok:
                # 1.出库使能复位
                with glock:
                    siemens_1500.write_bool_to_plc(38, enableByte, enableBit, 0)
                # 2.取件完成，更新立库储位为空
                update_warehouse_null(warehouse_url, position)              
                # 3.创建新的立库outandin版本库 
                create_new_warehouse_version('Out', '0'+str(position), source_material_list)
                # 4.POST提交到MES接口
                post_mes_warehouse()

            # 三、 当线边库放件完成时，更新线边库储位
            line_trigger = gloVar.line_put_ok_list[line_no-1]

            # logger.info('==line_trigger====')
            # logger.info(line_trigger)

            if line_trigger:
                # 1.更新线边库储位
                update_line_storage_bin(line_storage_url, position, source_material_list)
                # 2.创建新的线边库outandin版本库
                create_new_line_storage_version('In', 'LineStorage'+str(line_no), source_material_list)
                # 3.POST提交到MES接口
                post_mes_line_storage() 
                # 4.退出该物料上料循环
                break

            i += 1
            # logger.info('load_action i')
            # logger.info(i)
            # 跳出while,结束上料
            if i >= 3000:
                siemens_1500.write_bool_to_plc(38, enableByte, enableBit, 0)
                return
            time.sleep(0.2)

    logger.info('---load_action---end-------')
    print('---load_action---end-------')

# 下料动作流程
def unload_action(siemens_1500, line_no, positionByte, enableByte, enableBit, enable, glock):
    logger.info('---unload action----start-----')
    logger.info(datetime.datetime.now())
    print('---unload action----start-----')
    # with glock:
    #     siemens_1500.write_int_to_plc(38, positionByte, position)
    #     time.sleep(0.1)
    #     siemens_1500.write_bool_to_plc(38, enableByte, enableBit, enable)


    i = 0

    # 1.获取线边库托盘信息
    line_storage_url = line_storage_bin_url + str(line_no)
    r = requests.get(line_storage_url)
    return_json = r.json()
    line_storage_bin = return_json['data']
    # print(line_storage_bin)
    source_material_list = line_storage_bin[0]['materialList']
    source = line_storage_bin[0]['source']

    logger.info('source is:')
    logger.info(source)
    logger.info('materialList is:')
    logger.info(source_material_list)   
    
    # 2.更新线边库
    nullMaterialList = generate_line_storage_info_null(line_no)
    param = {'isEmpty': 1,
    'materialList': nullMaterialList,
    'source': 0
    }
    payload = json.dumps(param)
    logger.info('====line_storage_info_null_payload====')
    logger.info(payload)
    response_put = requests.put(line_storage_url, data=payload)
    logger.info('line_storage_info_null response_put')
    logger.info(response_put.json())
    # 3.创建linestorage outandin版本库
    create_new_line_storage_version('Out', 'LineStorage'+str(line_no), source_material_list)

    # 4.POST MES
    post_mes_line_storage()

    while True:
        # 放件完成，更新入库
        if gloVar.warehouse_put_ok:
            # 1.更新立库
            url = 'http://localhost:8088/v1/api/wms/warehouse/bin/' + str(source)
            param = {'isEmpty': 0,
            'materialList': source_material_list
            }
            payload = json.dumps(param)
            response_put = requests.put(url, data=payload)
            #2. 创建新warehouse outandin版本
            create_new_warehouse_version('In', '0'+str(source), source_material_list)
            # 3.POST MES
            post_mes_warehouse()
            # 4.退出下料流程
            break
        
        i += 1
        # logger.info('unload_action i')
        # logger.info(i)

        # 跳出while,结束入库
        if i >= 600:
            return
        time.sleep(0.2)   

    logger.info('---unload action---end-------')
    print('---unload action---end-------')     
