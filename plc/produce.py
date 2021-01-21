import requests
import json


from global_list import gloVar

material_storage_uri = 'http://localhost:8088/v1/api/wms/material_storage'
r = requests.get(material_storage_uri)
return_json = r.json()

material_storage = return_json['data']
# print(material_storage)

material_dict = {}
for i in material_storage:
    material_dict[i['materialCode']] = i['locatorCode']
# print(material_dict)

warehouse_bin_uri = 'http://localhost:8088/v1/api/wms/warehouse/bin/'

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
        if gloVar.wssArray[index-1]:
            return index

def pre_produce():
    global material_dict
    uri = 'http://172.16.1.62/aim-mes/open-api/order/produce/v1/list'

    r = requests.get(uri)
    return_json = r.json()
    print(return_json)

    return_data = return_json['data']
    print(return_data)

    seq_list = []
    for i in return_data:
        seq_list.append(i['seq'])
    seq_list_str = ','.join(seq_list)

    print(seq_list_str)

    pre_produce = return_data[0]
    id = pre_produce['id']
    productCode = pre_produce['productCode']
    seq = pre_produce['seq']

    materialList = pre_produce['materialList']
    signType = pre_produce['signType']
    signValue = pre_produce['signValue']

    print(id)
    print(productCode)
    print(seq)
    print(materialList)
    print(signType)
    print(signValue)

    positions = []
    for i in materialList:
        materialCode = i['materialCode']
        locatorCode = material_dict[materialCode]
        locatorList = locatorCode.split(',')

        locatorCode = return_locator_code(locatorList)

        positions.append(locatorCode)

    print(positions)

    out_list = []

    for position in positions:
        r = requests.get(warehouse_bin_uri + str(position))
        return_json = r.json()

        warehouse_bin = return_json['data']
        print(warehouse_bin)
        material_dict = json.loads(warehouse_bin[0]['materialList'])

        for key,value in material_dict.items():
            no = int(key)
            if value != 'null':
                return 

        length = material_dict.items()
        quantity = length - no

        out = {
            'position': position,
            'no': no,
            'quantity': quantity
        }

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


if __name__ == "__main__":
    pre_produce()