import json

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
  
def generate_plate_info_json(start, end, materialCode):
    temp_dict = {}
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
        {"id":1, "lineStorageCode": "LineStorage1", "isEmpty":True, "materialList":line_storage1_json},
        {"id":2, "lineStorageCode": "LineStorage2", "isEmpty":True, "materialList":line_storage2_json},
        {"id":3, "lineStorageCode": "LineStorage3", "isEmpty":True, "materialList":line_storage3_json},
        {"id":4, "lineStorageCode": "LineStorage4", "isEmpty":True, "materialList":line_storage4_json},
        {"id":5, "lineStorageCode": "LineStorage5", "isEmpty":True, "materialList":line_storage5_json},
        {"id":6, "lineStorageCode": "LineStorage6", "isEmpty":True, "materialList":line_storage6_json},   
    ]
    print(lineStorageValues)
    return lineStorageValues

