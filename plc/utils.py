import requests
import json
import datetime

def generate_materials_list():
    materialsList = [
        {"id":1, "materialCode": "Za01.01", "materialName": "白色充电款底壳", "materialClass":"Za01", "description":"底壳" },
        {"id":2, "materialCode": "Za01.02", "materialName": "黑色充电款底壳", "materialClass":"Za01", "description":"底壳" },
        {"id":3, "materialCode": "Za01.03", "materialName": "粉色充电款底壳", "materialClass":"Za01", "description":"底壳" },
        {"id":4, "materialCode": "Za01.04", "materialName": "白色电池款底壳", "materialClass":"Za01", "description":"底壳" },
        {"id":5, "materialCode": "Za01.05", "materialName": "黑色电池款底壳", "materialClass":"Za01", "description":"底壳" },
        {"id":6, "materialCode": "Za01.06", "materialName": "粉色电池款底壳", "materialClass":"Za01", "description":"底壳" },

        {"id":7, "materialCode": "Za02.01", "materialName": "白色充电款中壳", "materialClass":"Za02", "description":"中壳" },
        {"id":8, "materialCode": "Za02.02", "materialName": "黑色充电款中壳", "materialClass":"Za02", "description":"中壳" },
        {"id":9, "materialCode": "Za02.03", "materialName": "粉色充电款中壳", "materialClass":"Za02", "description":"中壳" },
        {"id":10, "materialCode": "Za02.04", "materialName": "白色电池款中壳", "materialClass":"Za02", "description":"中壳" },
        {"id":11, "materialCode": "Za02.05", "materialName": "黑色电池款中壳", "materialClass":"Za02", "description":"中壳" },
        {"id":12, "materialCode": "Za02.06", "materialName": "粉色电池款中壳", "materialClass":"Za02", "description":"中壳" },

        {"id":13, "materialCode": "Za03.01", "materialName": "白色充电款上壳", "materialClass":"Za03", "description":"上壳" },
        {"id":14, "materialCode": "Za03.02", "materialName": "黑色充电款上壳", "materialClass":"Za03", "description":"上壳" },
        {"id":15, "materialCode": "Za03.03", "materialName": "粉色充电款上壳", "materialClass":"Za03", "description":"上壳" },
        {"id":16, "materialCode": "Za03.04", "materialName": "白色电池款上壳", "materialClass":"Za03", "description":"上壳" },
        {"id":17, "materialCode": "Za03.05", "materialName": "黑色电池款上壳", "materialClass":"Za03", "description":"上壳" },
        {"id":18, "materialCode": "Za03.06", "materialName": "粉色电池款上壳", "materialClass":"Za03", "description":"上壳" },

        {"id":19, "materialCode": "Ba02.01", "materialName": "白色充电款电池盖", "materialClass":"Ba02", "description":"电池盖" },
        {"id":20, "materialCode": "Ba02.02", "materialName": "黑色充电款电池盖", "materialClass":"Ba02", "description":"电池盖" },
        {"id":21, "materialCode": "Ba02.03", "materialName": "粉色充电款电池盖", "materialClass":"Ba02", "description":"电池盖" },
        {"id":22, "materialCode": "Ba02.04", "materialName": "白色电池款电池盖", "materialClass":"Ba02", "description":"电池盖" },
        {"id":23, "materialCode": "Ba02.05", "materialName": "黑色电池款电池盖", "materialClass":"Ba02", "description":"电池盖" },
        {"id":24, "materialCode": "Ba02.06", "materialName": "粉色电池款电池盖", "materialClass":"Ba02", "description":"电池盖" },
        
        {"id":25, "materialCode": "Ba01.01", "materialName": "电池", "materialClass":"Ba01", "description":"电池" },
        
        {"id":26, "materialCode": "La01.01", "materialName": "公制螺丝", "materialClass":"La01", "description":"螺丝" },

        {"id":27, "materialCode": "Na01.01", "materialName": "包装盒", "materialClass":"Na01", "description":"包装盒" },
    ]
    return materialsList


def generate_material_storage_init():
    material_storage = [
        {"id":1, "materialCode": "Za01.01", "locatorCode": "7,8"},
        {"id":2, "materialCode": "Za01.02", "locatorCode": "9,10,11,12"},
        {"id":3, "materialCode": "Za01.03", "locatorCode": ""},
        {"id":4, "materialCode": "Za01.04", "locatorCode": "33,34"},
        {"id":5, "materialCode": "Za01.05", "locatorCode": "35,36,37,38"},
        {"id":6, "materialCode": "Za01.06", "locatorCode": ""},

        {"id":7, "materialCode": "Za02.01", "locatorCode": "13,14"},
        {"id":8, "materialCode": "Za02.02", "locatorCode": "15,16,17,18"},
        {"id":9, "materialCode": "Za02.03", "locatorCode": ""},
        {"id":10, "materialCode": "Za02.04", "locatorCode": "39,40"},
        {"id":11, "materialCode": "Za02.05", "locatorCode": "41,42,43,44"},
        {"id":12, "materialCode": "Za02.06", "locatorCode": ""},

        {"id":13, "materialCode": "Za03.01", "locatorCode": "19,20"},
        {"id":14, "materialCode": "Za03.02", "locatorCode": "21,22"},
        {"id":15, "materialCode": "Za03.03", "locatorCode": "23,24"},
        {"id":16, "materialCode": "Za03.04", "locatorCode": "45,46"},
        {"id":17, "materialCode": "Za03.05", "locatorCode": "47,48"},
        {"id":18, "materialCode": "Za03.06", "locatorCode": "49,50"},

        {"id":19, "materialCode": "Ba02.01", "locatorCode": "26,52"},
        {"id":20, "materialCode": "Ba02.02", "locatorCode": "26,52"},
        {"id":21, "materialCode": "Ba02.03", "locatorCode": "26,52"},
        {"id":22, "materialCode": "Ba02.04", "locatorCode": "26,52"},
        {"id":23, "materialCode": "Ba02.05", "locatorCode": "26,52"},
        {"id":24, "materialCode": "Ba02.06", "locatorCode": "26,52"},
        
        {"id":25, "materialCode": "Ba01.01", "locatorCode": "25,51"},
        
        {"id":26, "materialCode": "La01.01", "locatorCode": ""},

        {"id":27, "materialCode": "Na01.01", "locatorCode": "1,2,3,4,5,6,27,28,29,30,31,32"},
    ]

    return material_storage


def generate_plate_info_json(start, end, materialCode):
    temp_dict = {}
    for i in range(start, end):
        temp_dict[str(i)] = materialCode
    # print(temp_dict)
    temp_json = json.dumps(temp_dict)
    # print(temp_json)

    return temp_json


def generate_unload_plate_info_json(start, end, materialCode):
    temp_dict = {}
    for i in range(1, start):
        temp_dict[str(i)] = 'null'
    for i in range(start, end):
        temp_dict[str(i)] = materialCode
    # print(temp_dict)
    temp_json = json.dumps(temp_dict)
    # print(temp_json)

    return temp_json


def generate_warehouse_info():
    box_json = generate_plate_info_json(1,7,'Na01.01') 

    a_white_bottom_json = generate_plate_info_json(1,10,'Za01.01') 
    a_black_bottom_json = generate_plate_info_json(1,10,'Za01.02') 
    a_pink_bottom_json = generate_plate_info_json(1,10,'Za01.03') 
    a_white_middle_json = generate_plate_info_json(1,10,'Za02.01') 
    a_black_middle_json = generate_plate_info_json(1,10,'Za02.02') 
    a_pink_middle_json = generate_plate_info_json(1,10,'Za02.03') 
    a_white_up_json = generate_plate_info_json(1,10,'Za03.01') 
    a_black_up_json = generate_plate_info_json(1,10,'Za03.02') 
    a_pink_up_json = generate_plate_info_json(1,10,'Za03.03') 

    b_white_bottom_json = generate_plate_info_json(1,10,'Za01.04') 
    b_black_bottom_json = generate_plate_info_json(1,10,'Za01.05') 
    b_pink_bottom_json = generate_plate_info_json(1,10,'Za01.06') 
    b_white_middle_json = generate_plate_info_json(1,10,'Za01.04') 
    b_black_middle_json = generate_plate_info_json(1,10,'Za02.05') 
    b_pink_middle_json = generate_plate_info_json(1,10,'Za03.06') 
    b_white_up_json = generate_plate_info_json(1,10,'Za01.04') 
    b_black_up_json = generate_plate_info_json(1,10,'Za02.05') 
    b_pink_up_json = generate_plate_info_json(1,10,'Za03.06') 

    battery_json = generate_plate_info_json(1,55,'Ba01.01')

    battery_lid_dict = {}
    for i in range(1,29):
        battery_lid_dict[str(i)] = 'Ba02.01'
    for i in range(29,53):
        battery_lid_dict[str(i)] = 'Ba02.02'
    battery_lid_json = json.dumps(battery_lid_dict)

    warehouseValues = [
        {"id":1, "locatorCode": "001", "isEmpty":False, "materialList":box_json},
        {"id":2, "locatorCode": "002", "isEmpty":False, "materialList":box_json},
        {"id":3, "locatorCode": "003", "isEmpty":False, "materialList":box_json},
        {"id":4, "locatorCode": "004", "isEmpty":False, "materialList":box_json},
        {"id":5, "locatorCode": "005", "isEmpty":False, "materialList":box_json},
        {"id":6, "locatorCode": "006", "isEmpty":False, "materialList":box_json},

        {"id":7, "locatorCode": "007", "isEmpty":False, "materialList":a_black_bottom_json},
        {"id":8, "locatorCode": "008", "isEmpty":False, "materialList":a_black_bottom_json},
        {"id":9, "locatorCode": "009", "isEmpty":False, "materialList":a_white_bottom_json},
        {"id":10, "locatorCode": "010", "isEmpty":False, "materialList":a_white_bottom_json},
        {"id":11, "locatorCode": "011", "isEmpty":False, "materialList":a_white_bottom_json},
        {"id":12, "locatorCode": "012", "isEmpty":False, "materialList":a_white_bottom_json},

        {"id":13, "locatorCode": "013", "isEmpty":False, "materialList":a_black_middle_json},
        {"id":14, "locatorCode": "014", "isEmpty":False, "materialList":a_black_middle_json},
        {"id":15, "locatorCode": "015", "isEmpty":False, "materialList":a_white_middle_json},
        {"id":16, "locatorCode": "016", "isEmpty":False, "materialList":a_white_middle_json},
        {"id":17, "locatorCode": "017", "isEmpty":False, "materialList":a_white_middle_json},
        {"id":18, "locatorCode": "018", "isEmpty":False, "materialList":a_white_middle_json},

        {"id":19, "locatorCode": "019", "isEmpty":False, "materialList":a_black_up_json},
        {"id":20, "locatorCode": "020", "isEmpty":False, "materialList":a_black_up_json},
        {"id":21, "locatorCode": "021", "isEmpty":False, "materialList":a_white_up_json},
        {"id":22, "locatorCode": "022", "isEmpty":False, "materialList":a_white_up_json},
        {"id":23, "locatorCode": "023", "isEmpty":False, "materialList":a_pink_up_json},
        {"id":24, "locatorCode": "024", "isEmpty":False, "materialList":a_pink_up_json},

        {"id":25, "locatorCode": "025", "isEmpty":False, "materialList":battery_json},
        {"id":26, "locatorCode": "026", "isEmpty":False, "materialList":battery_lid_json},

        {"id":27, "locatorCode": "027", "isEmpty":False, "materialList":box_json},
        {"id":28, "locatorCode": "028", "isEmpty":False, "materialList":box_json},
        {"id":29, "locatorCode": "029", "isEmpty":False, "materialList":box_json},
        {"id":30, "locatorCode": "030", "isEmpty":False, "materialList":box_json},
        {"id":31, "locatorCode": "031", "isEmpty":False, "materialList":box_json},
        {"id":32, "locatorCode": "032", "isEmpty":False, "materialList":box_json},

        {"id":33, "locatorCode": "033", "isEmpty":False, "materialList":b_black_bottom_json},
        {"id":34, "locatorCode": "034", "isEmpty":False, "materialList":b_black_bottom_json},
        {"id":35, "locatorCode": "035", "isEmpty":False, "materialList":b_white_bottom_json},
        {"id":36, "locatorCode": "036", "isEmpty":False, "materialList":b_white_bottom_json},
        {"id":37, "locatorCode": "037", "isEmpty":False, "materialList":b_white_bottom_json},
        {"id":38, "locatorCode": "038", "isEmpty":False, "materialList":b_white_bottom_json},

        {"id":39, "locatorCode": "039", "isEmpty":False, "materialList":b_black_middle_json},
        {"id":40, "locatorCode": "040", "isEmpty":False, "materialList":b_black_middle_json},
        {"id":41, "locatorCode": "041", "isEmpty":False, "materialList":b_white_middle_json},
        {"id":42, "locatorCode": "042", "isEmpty":False, "materialList":b_white_middle_json},
        {"id":43, "locatorCode": "043", "isEmpty":False, "materialList":b_white_middle_json},
        {"id":44, "locatorCode": "044", "isEmpty":False, "materialList":b_white_middle_json},

        {"id":45, "locatorCode": "045", "isEmpty":False, "materialList":b_black_up_json},
        {"id":46, "locatorCode": "046", "isEmpty":False, "materialList":b_black_up_json},
        {"id":47, "locatorCode": "047", "isEmpty":False, "materialList":b_white_up_json},
        {"id":48, "locatorCode": "048", "isEmpty":False, "materialList":b_white_up_json},
        {"id":49, "locatorCode": "049", "isEmpty":False, "materialList":b_pink_up_json},
        {"id":50, "locatorCode": "050", "isEmpty":False, "materialList":b_pink_up_json},

        {"id":51, "locatorCode": "051", "isEmpty":False, "materialList":battery_json},
        {"id":52, "locatorCode": "052", "isEmpty":False, "materialList":battery_lid_json},    
    ]
    print(warehouseValues)
    return warehouseValues


def generate_warehouse_info_init():
    box_json = generate_plate_info_json(1,7,'null') 

    a_white_bottom_json = generate_plate_info_json(1,10,'null') 
    a_black_bottom_json = generate_plate_info_json(1,10,'null') 
    a_pink_bottom_json = generate_plate_info_json(1,10,'null') 
    a_white_middle_json = generate_plate_info_json(1,10,'null') 
    a_black_middle_json = generate_plate_info_json(1,10,'null') 
    a_pink_middle_json = generate_plate_info_json(1,10,'null') 
    a_white_up_json = generate_plate_info_json(1,10,'null') 
    a_black_up_json = generate_plate_info_json(1,10,'null') 
    a_pink_up_json = generate_plate_info_json(1,10,'null') 

    b_white_bottom_json = generate_plate_info_json(1,10,'null') 
    b_black_bottom_json = generate_plate_info_json(1,10,'null') 
    b_pink_bottom_json = generate_plate_info_json(1,10,'null') 
    b_white_middle_json = generate_plate_info_json(1,10,'null') 
    b_black_middle_json = generate_plate_info_json(1,10,'null') 
    b_pink_middle_json = generate_plate_info_json(1,10,'null') 
    b_white_up_json = generate_plate_info_json(1,10,'null') 
    b_black_up_json = generate_plate_info_json(1,10,'null') 
    b_pink_up_json = generate_plate_info_json(1,10,'null') 

    battery_json = generate_plate_info_json(1,55,'null')

    battery_lid_dict = {}
    for i in range(1,29):
        battery_lid_dict[str(i)] = 'null'
    for i in range(29,53):
        battery_lid_dict[str(i)] = 'null'
    battery_lid_json = json.dumps(battery_lid_dict)

    warehouseValues = [
        {"id":1, "locatorCode": "001", "isEmpty":True, "materialList":box_json},
        {"id":2, "locatorCode": "002", "isEmpty":True, "materialList":box_json},
        {"id":3, "locatorCode": "003", "isEmpty":True, "materialList":box_json},
        {"id":4, "locatorCode": "004", "isEmpty":True, "materialList":box_json},
        {"id":5, "locatorCode": "005", "isEmpty":True, "materialList":box_json},
        {"id":6, "locatorCode": "006", "isEmpty":True, "materialList":box_json},

        {"id":7, "locatorCode": "007", "isEmpty":True, "materialList":a_black_bottom_json},
        {"id":8, "locatorCode": "008", "isEmpty":True, "materialList":a_black_bottom_json},
        {"id":9, "locatorCode": "009", "isEmpty":True, "materialList":a_white_bottom_json},
        {"id":10, "locatorCode": "010", "isEmpty":True, "materialList":a_white_bottom_json},
        {"id":11, "locatorCode": "011", "isEmpty":True, "materialList":a_white_bottom_json},
        {"id":12, "locatorCode": "012", "isEmpty":True, "materialList":a_white_bottom_json},

        {"id":13, "locatorCode": "013", "isEmpty":True, "materialList":a_black_middle_json},
        {"id":14, "locatorCode": "014", "isEmpty":True, "materialList":a_black_middle_json},
        {"id":15, "locatorCode": "015", "isEmpty":True, "materialList":a_white_middle_json},
        {"id":16, "locatorCode": "016", "isEmpty":True, "materialList":a_white_middle_json},
        {"id":17, "locatorCode": "017", "isEmpty":True, "materialList":a_white_middle_json},
        {"id":18, "locatorCode": "018", "isEmpty":True, "materialList":a_white_middle_json},

        {"id":19, "locatorCode": "019", "isEmpty":True, "materialList":a_black_up_json},
        {"id":20, "locatorCode": "020", "isEmpty":True, "materialList":a_black_up_json},
        {"id":21, "locatorCode": "021", "isEmpty":True, "materialList":a_white_up_json},
        {"id":22, "locatorCode": "022", "isEmpty":True, "materialList":a_white_up_json},
        {"id":23, "locatorCode": "023", "isEmpty":True, "materialList":a_pink_up_json},
        {"id":24, "locatorCode": "024", "isEmpty":True, "materialList":a_pink_up_json},

        {"id":25, "locatorCode": "025", "isEmpty":True, "materialList":battery_json},
        {"id":26, "locatorCode": "026", "isEmpty":True, "materialList":battery_lid_json},

        {"id":27, "locatorCode": "027", "isEmpty":True, "materialList":box_json},
        {"id":28, "locatorCode": "028", "isEmpty":True, "materialList":box_json},
        {"id":29, "locatorCode": "029", "isEmpty":True, "materialList":box_json},
        {"id":30, "locatorCode": "030", "isEmpty":True, "materialList":box_json},
        {"id":31, "locatorCode": "031", "isEmpty":True, "materialList":box_json},
        {"id":32, "locatorCode": "032", "isEmpty":True, "materialList":box_json},

        {"id":33, "locatorCode": "033", "isEmpty":True, "materialList":b_black_bottom_json},
        {"id":34, "locatorCode": "034", "isEmpty":True, "materialList":b_black_bottom_json},
        {"id":35, "locatorCode": "035", "isEmpty":True, "materialList":b_white_bottom_json},
        {"id":36, "locatorCode": "036", "isEmpty":True, "materialList":b_white_bottom_json},
        {"id":37, "locatorCode": "037", "isEmpty":True, "materialList":b_white_bottom_json},
        {"id":38, "locatorCode": "038", "isEmpty":True, "materialList":b_white_bottom_json},

        {"id":39, "locatorCode": "039", "isEmpty":True, "materialList":b_black_middle_json},
        {"id":40, "locatorCode": "040", "isEmpty":True, "materialList":b_black_middle_json},
        {"id":41, "locatorCode": "041", "isEmpty":True, "materialList":b_white_middle_json},
        {"id":42, "locatorCode": "042", "isEmpty":True, "materialList":b_white_middle_json},
        {"id":43, "locatorCode": "043", "isEmpty":True, "materialList":b_white_middle_json},
        {"id":44, "locatorCode": "044", "isEmpty":True, "materialList":b_white_middle_json},

        {"id":45, "locatorCode": "045", "isEmpty":True, "materialList":b_black_up_json},
        {"id":46, "locatorCode": "046", "isEmpty":True, "materialList":b_black_up_json},
        {"id":47, "locatorCode": "047", "isEmpty":True, "materialList":b_white_up_json},
        {"id":48, "locatorCode": "048", "isEmpty":True, "materialList":b_white_up_json},
        {"id":49, "locatorCode": "049", "isEmpty":True, "materialList":b_pink_up_json},
        {"id":50, "locatorCode": "050", "isEmpty":True, "materialList":b_pink_up_json},

        {"id":51, "locatorCode": "051", "isEmpty":True, "materialList":battery_json},
        {"id":52, "locatorCode": "052", "isEmpty":True, "materialList":battery_lid_json},    
    ]
    print(warehouseValues)
    return warehouseValues


def generate_line_storage_info():
    line_storage1_json = generate_plate_info_json(1,10,'Za01.01')
    line_storage2_json = generate_plate_info_json(1,10,'Za02.01')
    line_storage3_json = generate_plate_info_json(1,10,'Za03.01')
    line_storage4_json = generate_plate_info_json(1,55,'Ba01.01')
    line_storage5_json = generate_plate_info_json(1,53,'Ba02.01')
    line_storage6_json = generate_plate_info_json(1,7,'Na01.01')

    lineStorageValues = [
        {"id":1, "lineStorageCode": "LineStorage1", "isEmpty":False, "materialList":line_storage1_json},
        {"id":2, "lineStorageCode": "LineStorage2", "isEmpty":False, "materialList":line_storage2_json},
        {"id":3, "lineStorageCode": "LineStorage3", "isEmpty":False, "materialList":line_storage3_json},
        {"id":4, "lineStorageCode": "LineStorage4", "isEmpty":False, "materialList":line_storage4_json},
        {"id":5, "lineStorageCode": "LineStorage5", "isEmpty":False, "materialList":line_storage5_json},
        {"id":6, "lineStorageCode": "LineStorage6", "isEmpty":False, "materialList":line_storage6_json},   
    ]
    print(lineStorageValues)
    return lineStorageValues


def generate_line_storage_info_init():
    line_storage1_json = generate_plate_info_json(1,10,'null')
    line_storage2_json = generate_plate_info_json(1,10,'null')
    line_storage3_json = generate_plate_info_json(1,10,'null')
    line_storage4_json = generate_plate_info_json(1,55,'null')
    line_storage5_json = generate_plate_info_json(1,53,'null')
    line_storage6_json = generate_plate_info_json(1,7,'null')

    lineStorageValues = [
        {"id":1, "lineStorageCode": "LineStorage1", "isEmpty":True, "materialList":line_storage1_json, "source":0},
        {"id":2, "lineStorageCode": "LineStorage2", "isEmpty":True, "materialList":line_storage2_json, "source":0},
        {"id":3, "lineStorageCode": "LineStorage3", "isEmpty":True, "materialList":line_storage3_json, "source":0},
        {"id":4, "lineStorageCode": "LineStorage4", "isEmpty":True, "materialList":line_storage4_json, "source":0},
        {"id":5, "lineStorageCode": "LineStorage5", "isEmpty":True, "materialList":line_storage5_json, "source":0},
        {"id":6, "lineStorageCode": "LineStorage6", "isEmpty":True, "materialList":line_storage6_json, "source":0},   
    ]
    print(lineStorageValues)
    return lineStorageValues


def generate_line_storage_info_null(lineStorageCode):
    if lineStorageCode == 1:
        line_storage_json = generate_plate_info_json(1,10,'null')
    elif lineStorageCode == 2:
        line_storage_json = generate_plate_info_json(1,10,'null')
    elif lineStorageCode == 3:
        line_storage_json = generate_plate_info_json(1,10,'null')
    elif lineStorageCode == 4:
        line_storage_json = generate_plate_info_json(1,55,'null')
    elif lineStorageCode == 5:
        line_storage_json = generate_plate_info_json(1,53,'null')
    elif lineStorageCode == 6:
        line_storage_json = generate_plate_info_json(1,7,'null')
    else:
        print('generate_line_storage_info_null error!')
    return line_storage_json


def generate_linestorage_no(bin_id):
    if bin_id >= 1 and bin_id <= 6 or bin_id >= 27 and bin_id <= 32:
        # 包装盒
        line_no = 6
    elif bin_id >= 7 and bin_id <= 12 or bin_id >= 33 and bin_id <= 38:
        # 下盖
        line_no = 1
    elif bin_id >= 13 and bin_id <= 18 or bin_id >= 39 and bin_id <= 44:
        # 中盖
        line_no = 2
    elif bin_id >= 19 and bin_id <= 24 or bin_id >= 45 and bin_id <= 50:
        # 上盖
        line_no = 3
    elif bin_id == 25 or bin_id == 51:
        # 电池
        line_no = 4
    elif bin_id == 26 or bin_id == 52:
        # 电池盖
        line_no = 5
    else:
        line_no = 0

    return line_no                      


def get_material_dict():
    material_storage_uri = 'http://localhost:8088/v1/api/wms/material_storage'
    r = requests.get(material_storage_uri)
    return_json = r.json()

    material_storage = return_json['data']
    # print(material_storage)

    material_dict = {}
    for i in material_storage:
        locatorCodeList = i['locatorCode'].split(',')
        material_dict[i['materialCode']] = locatorCodeList
    # print(material_dict)
    return material_dict


def generate_material_list_json(bin_id，quantity):
    
    if bin_id >= 1 and bin_id <= 6 or bin_id >= 27 and bin_id <= 32:
        materialList = generate_plate_info_json(quantity，7, 'Na01.01') 
    elif bin_id >= 7 and bin_id <= 8:
        materialList = generate_plate_info_json(quantity，10, "Za01.01") 
    elif bin_id >= 9 and bin_id <= 10:
        materialList = generate_plate_info_json(quantity，10, "Za01.02")
    elif bin_id >= 11 and bin_id <= 12:
        materialList = generate_plate_info_json(quantity，10, "Za01.03")  
    elif bin_id >= 13 and bin_id <= 14:
        materialList = generate_plate_info_json(quantity，10, "Za02.01") 
    elif bin_id >= 15 and bin_id <= 16:
        materialList = generate_plate_info_json(quantity，10, "Za02.02")
    elif bin_id >= 17 and bin_id <= 18:
        materialList = generate_plate_info_json(quantity，10, "Za02.03") 
    elif bin_id >= 19 and bin_id <= 20:
        materialList = generate_plate_info_json(quantity，10, "Za03.01") 
    elif bin_id >= 21 and bin_id <= 22:
        materialList = generate_plate_info_json(quantity，10, "Za03.02")
    elif bin_id >= 23 and bin_id <= 24:
        materialList = generate_plate_info_json(quantity，10, "Za03.03")       
    elif bin_id == 25 or bin_id == 51:
        materialList = generate_plate_info_json(quantity，55, 'Ba01.01') 
    elif bin_id == 26 or bin_id == 52:
        materialList = generate_plate_info_json(quantity，53, 'Ba02.05') 

    elif bin_id >= 33 and bin_id <= 34:
        materialList = generate_plate_info_json(quantity，10, "Za01.04") 
    elif bin_id >= 35 and bin_id <= 36:
        materialList = generate_plate_info_json(quantity，10, "Za01.05")
    elif bin_id >= 37 and bin_id <= 38:
        materialList = generate_plate_info_json(quantity，10, "Za01.06")  
    elif bin_id >= 39 and bin_id <= 40:
        materialList = generate_plate_info_json(quantity，10, "Za02.04") 
    elif bin_id >= 41 and bin_id <= 42:
        materialList = generate_plate_info_json(quantity，10, "Za02.05")
    elif bin_id >= 43 and bin_id <= 44:
        materialList = generate_plate_info_json(quantity，10, "Za02.06") 
    elif bin_id >= 45 and bin_id <= 46:
        materialList = generate_plate_info_json(quantity，10, "Za03.04") 
    elif bin_id >= 47 and bin_id <= 48:
        materialList = generate_plate_info_json(quantity，10, "Za03.05")
    elif bin_id >= 49 and bin_id <= 50:
        materialList = generate_plate_info_json(quantity，10, "Za03.06") 

    else:
        print('unknown!')

    print(materialList)

    return materialList


def generate_unload_material_list_json(quantity, bin_id):
    
    if bin_id >= 1 and bin_id <= 6 or bin_id >= 27 and bin_id <= 32:
        materialList = generate_unload_plate_info_json(quantity,7, 'Na01.01') 
    elif bin_id >= 7 and bin_id <= 8:
        materialList = generate_unload_plate_info_json(quantity,10, "Za01.01") 
    elif bin_id >= 9 and bin_id <= 10:
        materialList = generate_unload_plate_info_json(quantity,10, "Za01.02")
    elif bin_id >= 11 and bin_id <= 12:
        materialList = generate_unload_plate_info_json(quantity,10, "Za01.03")  
    elif bin_id >= 13 and bin_id <= 14:
        materialList = generate_unload_plate_info_json(quantity,10, "Za02.01") 
    elif bin_id >= 15 and bin_id <= 16:
        materialList = generate_unload_plate_info_json(quantity,10, "Za02.02")
    elif bin_id >= 17 and bin_id <= 18:
        materialList = generate_unload_plate_info_json(quantity,10, "Za02.03") 
    elif bin_id >= 19 and bin_id <= 20:
        materialList = generate_unload_plate_info_json(quantity,10, "Za03.01") 
    elif bin_id >= 21 and bin_id <= 22:
        materialList = generate_unload_plate_info_json(quantity,10, "Za03.02")
    elif bin_id >= 23 and bin_id <= 24:
        materialList = generate_unload_plate_info_json(quantity,10, "Za03.03")       
    elif bin_id == 25 or bin_id == 51:
        materialList = generate_unload_plate_info_json(quantity,55, 'Ba01.01') 
    elif bin_id == 26 or bin_id == 52:
        materialList = generate_unload_plate_info_json(quantity,53, 'Ba02.04') 

    elif bin_id >= 33 and bin_id <= 34:
        materialList = generate_unload_plate_info_json(quantity,10, "Za01.04") 
    elif bin_id >= 35 and bin_id <= 36:
        materialList = generate_unload_plate_info_json(quantity,10, "Za01.05")
    elif bin_id >= 37 and bin_id <= 38:
        materialList = generate_unload_plate_info_json(quantity,10, "Za01.06")  
    elif bin_id >= 39 and bin_id <= 40:
        materialList = generate_unload_plate_info_json(quantity,10, "Za01.04") 
    elif bin_id >= 41 and bin_id <= 42:
        materialList = generate_unload_plate_info_json(quantity,10, "Za01.05")
    elif bin_id >= 43 and bin_id <= 44:
        materialList = generate_unload_plate_info_json(quantity,10, "Za01.06") 
    elif bin_id >= 45 and bin_id <= 46:
        materialList = generate_unload_plate_info_json(quantity,10, "Za03.04") 
    elif bin_id >= 47 and bin_id <= 48:
        materialList = generate_unload_plate_info_json(quantity,10, "Za03.05")
    elif bin_id >= 49 and bin_id <= 50:
        materialList = generate_unload_plate_info_json(quantity,10, "Za03.06") 

    else:
        print('unknown!')

    print(materialList)

    return materialList

def generate_null_material_list_json(bin_id):
    
    if bin_id >= 1 and bin_id <= 6 or bin_id >= 27 and bin_id <= 32:
        materialList = generate_plate_info_json(1,7, 'null') 
    elif bin_id >= 7 and bin_id <= 8:
        materialList = generate_plate_info_json(1,10, "null") 
    elif bin_id >= 9 and bin_id <= 10:
        materialList = generate_plate_info_json(1,10, "null")
    elif bin_id >= 11 and bin_id <= 12:
        materialList = generate_plate_info_json(1,10, "null")  
    elif bin_id >= 13 and bin_id <= 14:
        materialList = generate_plate_info_json(1,10, "null") 
    elif bin_id >= 15 and bin_id <= 16:
        materialList = generate_plate_info_json(1,10, "null")
    elif bin_id >= 17 and bin_id <= 18:
        materialList = generate_plate_info_json(1,10, "null") 
    elif bin_id >= 19 and bin_id <= 20:
        materialList = generate_plate_info_json(1,10, "null") 
    elif bin_id >= 21 and bin_id <= 22:
        materialList = generate_plate_info_json(1,10, "null")
    elif bin_id >= 23 and bin_id <= 24:
        materialList = generate_plate_info_json(1,10, "null")       
    elif bin_id == 25 or bin_id == 51:
        materialList = generate_plate_info_json(1,55, 'null') 
    elif bin_id == 26 or bin_id == 52:
        materialList = generate_plate_info_json(1,53, 'null') 

    elif bin_id >= 33 and bin_id <= 34:
        materialList = generate_plate_info_json(1,10, "null") 
    elif bin_id >= 35 and bin_id <= 36:
        materialList = generate_plate_info_json(1,10, "null")
    elif bin_id >= 37 and bin_id <= 38:
        materialList = generate_plate_info_json(1,10, "null")  
    elif bin_id >= 39 and bin_id <= 40:
        materialList = generate_plate_info_json(1,10, "null") 
    elif bin_id >= 41 and bin_id <= 42:
        materialList = generate_plate_info_json(1,10, "null")
    elif bin_id >= 43 and bin_id <= 44:
        materialList = generate_plate_info_json(1,10, "null") 
    elif bin_id >= 45 and bin_id <= 46:
        materialList = generate_plate_info_json(1,10, "null") 
    elif bin_id >= 47 and bin_id <= 48:
        materialList = generate_plate_info_json(1,10, "null")
    elif bin_id >= 49 and bin_id <= 50:
        materialList = generate_plate_info_json(1,10, "null") 

    else:
        print('unknown!')

    print(materialList)

    return materialList


def generate_warehouse_version_init():

    param = {'action': 'In',
        'positionCode': '007',
        'materialList': generate_plate_info_json(1,10, 'null') ,
        'created_date': datetime.datetime.now()
    }                

    warehouse_version = [param,]
    return warehouse_version

def generate_linestorage_version_init():
    param = {'action': 'Out',
        'positionCode': 'LineStorage1',
        'materialList': generate_plate_info_json(1,10, 'null') ,
        'created_date': datetime.datetime.now()
    }          
    linestorage_version = [param,]
    return linestorage_version

def bcd_to_int(x):
    """
    This translates binary coded decimal into an integer
    TODO - more efficient algorithm
    >>> bcd_to_int(4)
    4
    >>> bcd_to_int(159)
    345
    """

    if x < 0:
        raise ValueError("Cannot be a negative integer")

    binstring = ''
    while True:
        q, r = divmod(x, 10)
        nibble = bin(r).replace('0b', "")
        while len(nibble) < 4:
            nibble = '0' + nibble
        binstring = nibble + binstring
        if q == 0:
            break
        else:
            x = q

    return int(binstring, 2)


def int_to_bcd(x):
    """
    This translates an integer into
    binary coded decimal
    >>> int_to_bcd(4)
    4
    >>> int_to_bcd(34)
    22
    
    >>> int_to_bcd(0)
    0
    """

    if x < 0:
        raise ValueError("Cannot be a negative integer")
        
    if x == 0:
        return 0
        
    bcdstring = ''
    while x > 0:
        nibble = x % 16
        bcdstring = str(nibble) + bcdstring
        x >>= 4
    return int(bcdstring)


def bcd2time(x):
    return int(x[0:4], 2)*10 + int(x[4:8], 2)


def byte2string(x):
    return 'xx'


def checksum(x):
    cs = 0
    for i in range(len(x)):
        cs = cs + x[i]
    # print(cs%256)
    return cs%256


def num2bcd(num):
    a = (num % 10) & 0x0f
    print(a)
    b = ((num // 10) << 4) & 0xf0
    bcd = a | b
    return bcd


# def int2bitarray_8(int_, length):
#     a=  bin(int_)
#     b = a[2:]
#     c= [i for i in b]
#     if len(c) < length:
#         c = extend_list(c, length)
#     d = [True if i == '1' else False for i in c]
#     e = d[::-1]

#     return e

# def int2bitarray_16(int_, length):
#     a=  bin(int_)
#     b = a[2:]
#     c= [i for i in b]
#     if len(c) < length:
#         c = extend_list(c, length)
#     d = [True if i == '1' else False for i in c]
#     e = d[::-1]
#     print(e)
#     f = e[-8:].extend(e[0:8])
#     print(f)
#     return f 

# def int2bitarray_32(int_, length):
#     a=  bin(int_)
#     b = a[2:]
#     c= [i for i in b]
#     if len(c) < length:
#         c = extend_list(c, length)
#     d = [True if i == '1' else False for i in c]
#     e = d[::-1]
#     f = e[-8:].extend(e[0:8])
#     return f 





# def extend_list(list_, length):
#     d = ['0' for i in range(length-len(list_))]
#     d.extend(list_)
#     return d


def int2bitarray(int_, length):
    try:
        a =int_
        b=[]
        while 1:
            c,d = divmod(a,2)
            a = c
            b.append(d)
            if c < 2:
                b.append(c)
                break

        if len(b) < length:
            d = [0 for i in range(length-len(b))]
            b.extend(d)

        # print('---len(b)----')
        # print(len(b))
        # print(b)

        if length <=8:
            return true_false_0_1(b)

        elif length > 8 and length <=16:
            e = b[8:]
            e.extend(b[0:8])
            return true_false_0_1(b)

        elif length >16 and length <= 32:
            f = b[0:8]
            g = b[8:16]
            h = b[16:24]
            i = b[24:32]

            f.extend(g)
            f.extend(h)
            f.extend(i)

            return true_false_0_1(b)

    except  Exception as e:
        pass
        
# def true_false_0_1(list_):
#     return [True if i == 1 else False for i in list_]


def true_false_0_1(list_):
    return [1 if i == 1 else 0 for i in list_]