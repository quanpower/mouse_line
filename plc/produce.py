import requests
import json
import time
from global_list import gloVar
import operator
import threading 
from RobotActionLock import in_action, out_action, load_action, unload_action
from utils import get_material_dict


warehouse_bin_uri = 'http://localhost:8088/v1/api/wms/warehouse/bin/'

material_dict = get_material_dict()
print(material_dict)

def return_materials_position():

    materials_position = {
        'A': {
            'box': [1,2,3,4,5,6],
            'bottom': {
                'black': [7,8],
                'white': [9,10],
                'pink': [11,12]
            },
            'middle': {
                'black': [13,14],
                'white': [15,16],
                'pink': [17,18]                                    
            },
            'up': {
                'black': [19,20],
                'white': [21,22],
                'pink': [23,24]                                    
            },
            'battery': [25],
            'battery_lid': [26],                                 
        },
        'B': {
            'box': [27,28,29,30,31,32],
            'bottom': {
                'black': [33,34],
                'white': [35,36],
                'pink': [37,38]
            },
            'middle': {
                'black': [39,40],
                'white': [41,42],
                'pink': [43,44]                                    
            },
            'up': {
                'black': [45,46],
                'white': [47,48],
                'pink': [49,50]                                    
            },    
            'battery': [51],
            'battery_lid': [52],                             
        }
    }
    return materials_position

def return_locator_code(locatorList):

    for j in locatorList:
        index = int(j)
        # print(index)
        # print(gloVar.wssArray)
        if gloVar.wssArray[index-1]:
            return index

def get_order_list():
    uri = 'http://172.16.1.62/aim-mes/open-api/order/produce/v1/list'
    r = requests.get(uri)
    return_json = r.json()
    # print(return_json)
    order_list = return_json['data']
    # print(order_list)

    sorted_order_list = sorted(order_list, key=operator.itemgetter('seq'))
    print(sorted_order_list)
    return sorted_order_list

def pre_produce(order_list, siemens_1500, glock):
    
    global material_dict

    seq_list = []
    for i in order_list:
        seq_list.append(i['seq'])
    seq_list_str = ','.join(seq_list)

    print(seq_list_str)

    pre_produce = order_list[0]
    id = pre_produce['id']
    productCode = pre_produce['productCode']
    seq = pre_produce['seq']
    materialList = pre_produce['materialList']
    signType = pre_produce['signType']
    signValue = pre_produce['signValue']

    # print(id)
    # print(productCode)
    # print(seq)
    # print(materialList)
    # print(signType)
    # print(signValue)

    positions = []
    for i in materialList:
        materialCode = i['materialCode']
        locatorList = material_dict[materialCode]
        print('\n'*3)
        print(locatorList)
        locatorCode = return_locator_code(locatorList)
        print('===locatorCode===')
        print(locatorCode)
        positions.append(locatorCode)
    print('===positions===')
    print(positions)

    out_list = []

    for position in positions:
        if position:
            r = requests.get(warehouse_bin_uri + str(position))
            return_json = r.json()
            print(return_json)

            warehouse_bin = return_json['data']
            print(warehouse_bin)
            material_dict = json.loads(warehouse_bin[0]['materialList'])
            print('====material_dict===')
            print(material_dict)

            for key,value in material_dict.items():
                no = int(key)
                if value != 'null':
                    return 

            print(position)
            print(no)

            length = len(material_dict.items())
            print(length)

            quantity = length - no

            out = {
                'position': position,
                'no': no,
                'quantity': quantity
            }
            print(out)

            if quantity > 0:
                out_list.append(out)

    print(out_list)

    positionByte = 6
    noByte = 94
    quantityByte = 96
    enableByte = 4
    enableBit = 0
    enable = 1

    if out_list:
        thread_load = threading.Thread(name="thread_load", target=load_action, args=(siemens_1500, positionByte,noByte,quantityByte, enableByte, enableBit, enable,out_list, glock))
        thread_load.start()

def produce(glock):
    siemens_1500 =  gloVar.siemens_1500

    gloVar.material_dict = material_dict

    while True:
        order_list = get_order_list()
        if not gloVar.producing :
            pre_produce(order_list, siemens_1500, glock)

        time.sleep(100)

