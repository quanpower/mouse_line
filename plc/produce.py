import os
import requests
import json
import time
import datetime

import operator
import threading 
from RobotActionLock import in_action, out_action, load_action, unload_action
from utils import get_material_dict
import logging
from laser_client import client_send

logger = logging.getLogger(__name__)

from global_list import gloVar

material_dict = get_material_dict()
# print(material_dict)

# 获取预生产订单列表
def get_order_list():
    uri = 'http://172.16.1.62/aim-mes/open-api/order/produce/v1/list'

    try:
        r = requests.get(uri)
        return_json = r.json()
        order_list = return_json['data']
        sorted_order_list = sorted(order_list, key=operator.itemgetter('seq'))
        # print(sorted_order_list)
        return sorted_order_list
    except Exception as e:
        print(e)


# 返回取第几个储位
def return_locator_code(locatorList):
    for j in locatorList:
        index = int(j)
        # print(index)
        # print(gloVar.wssArray)
        if gloVar.wssArray[index-1]:
            return index


# 返回从托盘第几个位置开始抓取
def get_plate_no(plate_dict):
    for key,value in plate_dict.items():
        no = int(key)
        if value != 'null':
            return no
    return 1


# 生成订单列表字符串
def generate_seqliststr(order_list):
    seq_list = []
    for i in order_list:
        seq_list.append(i['seq'])
    seq_list_str = ','.join(seq_list)

    print('=====seq_list_str===')    
    print(seq_list_str)
    logger.info('=====seq_list_str===')
    logger.info(seq_list_str)
    return seq_list_str


# 根据物料清单生成线边库号
def get_line_storage_code(materialCode):
    materialCodeClass = materialCode[:4]
    if materialCodeClass == 'Za01':
         line_storage_code = 1
    elif materialCodeClass == 'Za02':
         line_storage_code = 2
    elif materialCodeClass == 'Za03':
         line_storage_code = 3
    elif materialCodeClass == 'Ba01':
         line_storage_code = 4
    elif materialCodeClass == 'Ba02':
         line_storage_code = 5
    elif materialCodeClass == 'Na01':
         line_storage_code = 6
    else:
        line_storage_code = 0
        print('error!')

    return line_storage_code


# 激光打印签名
def send_sign_to_laser(productCode, signType, signValue):
    if signType == 0:
        print('none to laser!')
    elif signType == 1:
        print('text to laser!')
        '''A:GDM1=ABC123*GDM2=123ABC*JPG=D:\PLT\tongjian.jpg'''
        data = productCode[:1]+':GDM1=' + signValue
        print(data)
        logger.info('====text to laser!===')
        logger.info(data)
        thread_laser = threading.Thread(name="thread_laser", target=client_send, args=(data,))
        thread_laser.start()         
    elif signType == 2:
        print('jpeg to laser!')
        file_name = os.path.basename(signValue)
        file_path = "D:\\PLT\\" + file_name
        print(signValue)
        print(file_path)
        try:
            response = requests.get(signValue)
            # 获取的文本实际上是图片的二进制文本
            img = response.content
            # 将他拷贝到本地文件 w 写  b 二进制  wb代表写入二进制文本
            with open( file_path,'wb' ) as f:
                f.write(img)

            data = productCode[:1]+ ":JPG=" + file_path
            logger.info('====jpeg to laser!===')
            logger.info(data)        
            thread_laser = threading.Thread(name="thread_laser", target=client_send, args=(data,))
            thread_laser.start()  
        except Exception as e:
            logger.info("jpeg to laser error!")
 

# 生成物料位置列表
def generate_positions(order_list):
    global material_dict
    try:
        pre_produce = order_list[0]
        id = pre_produce['id']
        productCode = pre_produce['productCode']
        seq = pre_produce['seq']
        materialList = pre_produce['materialList']
        signType = pre_produce['signType']
        signValue = pre_produce['signValue']
        
        send_sign_to_laser(productCode, signType, signValue)


        # 更新全局生产订单状态
        gloVar.orderNo = seq
        gloVar.productNo = productCode
        gloVar.state = 1
        gloVar.startTime = time.time()

        positions = []
        for i in materialList:
            materialCode = i['materialCode']

            line_storage_code = get_line_storage_code(materialCode)
            index = line_storage_code -1

            try:
                # 检测线边库工位无料盘才追加
                if not gloVar.plate_check_list[index]:
                    locatorList = material_dict[materialCode]
                    # print('\n'*3)
                    # print(locatorList)
                    locatorCode = return_locator_code(locatorList)
                    # print('===locatorCode===')
                    # print(locatorCode)
                    positions.append(locatorCode)
            except Exception as e:
                logger.info('generate_positions error')
                logger.info(e)                     

        logger.info('\n'*3)
        logger.info('===positions===')
        logger.info(positions)

        return positions

    except Exception as e:
        logger.info('generate_positions error')
        logger.info(e) 


# 生成上料出库列表
def generate_out_list(warehouse_bin_uri, positions):
    try:
        out_list = []

        for position in positions:
            if position:
                r = requests.get(warehouse_bin_uri + str(position))
                return_json = r.json()
                warehouse_bin = return_json['data']
                plate_dict = json.loads(warehouse_bin[0]['materialList'])
                # print('====plate_dict===')
                # print(plate_dict)

                no = get_plate_no(plate_dict)
                length = len(plate_dict.items())
                quantity = length - no + 1

                out = {
                    'position': position,
                    'no': no,
                    'quantity': quantity
                }

                if quantity > 0:
                    out_list.append(out)

        print('=========out_list========')
        print(out_list)
        logger.info('=========out_list========')
        logger.info(out_list)

        return out_list
    except Exception as e:
        logger.info('generate_out_list error')
        logger.info(e)


def pre_load(order_list, siemens_1500, glock):
    warehouse_bin_uri = 'http://localhost:8088/v1/api/wms/warehouse/bin/'    
    seq_list_str = generate_seqliststr(order_list)
    print(seq_list_str)

    positions = generate_positions(order_list)
    out_list = generate_out_list(warehouse_bin_uri, positions)

    positionByte = 6
    noByte = 94
    quantityByte = 96
    enableByte = 4
    enableBit = 0
    enable = 1

    seq = gloVar.orderNo
    productCode = gloVar.productNo

    if out_list:
        thread_load = threading.Thread(name="thread_load", target=load_action, args=(siemens_1500, positionByte, noByte, quantityByte, enableByte, enableBit, enable, out_list, seq, productCode, glock))
        thread_load.start()


def pre_unload(siemens_1500, line_no, glock):
    positionByte = 2
    enableByte = 1
    enableBit = 0
    enable = 1
    thread_unload = threading.Thread(name="thread_unload", target=unload_action, args=(siemens_1500, line_no, positionByte,  enableByte, enableBit, enable, glock))
    thread_unload.start()


def pre_in():
    pass


def pre_out():
    pass


def load_trigger(glock):
    siemens_1500 =  gloVar.siemens_1500

    gloVar.material_dict = material_dict

    while True:
        order_list = get_order_list()
        # 有新订单时
        if order_list:
            if gloVar.pre_order_ok:
                print('===load_trigger===')
                logger.info('===load_trigger===')
                pre_load(order_list, siemens_1500, glock)

        time.sleep(10)


def unload_trigger(glock):
    siemens_1500 =  gloVar.siemens_1500

    while True:
        if any(gloVar.line_get_ok_list):
            line_no = gloVar.line_get_ok_list.index(True) + 1
            logger.info('=====unload_trigger  line_no=====')
            logger.info(line_no)
            pre_unload(siemens_1500, line_no, glock)
        time.sleep(0.5)


def out_trigger(glock):
    siemens_1500 =  gloVar.siemens_1500
    while True:
        if False :
            # 托盘全空
            pre_out()
        time.sleep(1)


def in_trigger(glock):
    siemens_1500 =  gloVar.siemens_1500
    while True:
        if False :
            pre_in()
        time.sleep(1)