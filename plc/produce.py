import requests
import json
import time
from global_list import gloVar
import operator

warehouse_bin_uri = 'http://localhost:8088/v1/api/wms/warehouse/bin/'

def get_material_dict():
    material_storage_uri = 'http://localhost:8088/v1/api/wms/material_storage'
    r = requests.get(material_storage_uri)
    return_json = r.json()

    material_storage = return_json['data']
    # print(material_storage)

    material_dict = {}
    for i in material_storage:
        material_dict[i['materialCode']] = i['locatorCode']
    # print(material_dict)
    return material_dict

material_dict = get_material_dict()

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

def pre_produce(order_list):
    
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
        locatorCode = material_dict[materialCode]
        locatorList = locatorCode.split(',')
        print('\n'*3)
        print(locatorCode)
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
            print(length)

            length = material_dict.items()
            quantity = length - no

            out = {
                'position': position,
                'no': no,
                'quantity': quantity
            }
            print(out)

            out_list.append(out)

    print(out_list)

    positionByte = 6
    noByte = 94
    quantityByte = 96
    enableByte = 4
    enableBit = 0
    enable = 1

    if out_list:
        thread_out = threading.Thread(name="thread_out", target=load_action, args=(siemens_1500, positionByte,noByte,quantityByte, enableByte, enableBit, enable,out_list, glock))
        thread_out.start()

def produce():
    while True:
        order_list = get_order_list()
        if not gloVar.producing :
            pre_produce(order_list)
        time.sleep(100)

if __name__ == "__main__":
    wssArray = gloVar.wssArray
    get_order_list()