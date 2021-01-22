#!/usr/bin/python
# -*- coding: utf-8 -*-

class gloVar():
    siemens_1500 = None
    plc_disconnected = False
    sockets = {}
    warehouse_senser_status = []
    camera_triggers = [0,0,0,0,0,0,0,0]
    robot_status = []
    wssArray = []
    category = 'B'
    quantity = 0
    ready_ok = False

    material_dict = []
    
    warehouse_get_ok = False
    warehouse_put_ok = False
    line_get_ok_list = []
    line_put_ok_list = []
    plate_check_list = []
    
    ua_order_list = []
    
    # z2_get_ok = False
    # z2_put_ok = False

    # z3_get_ok = False
    # z3_put_ok = False
    # z4_get_ok = False
    # z4_put_ok = False         
    # z5_get_ok = False
    # z5_put_ok = False
    # z6_get_ok = False
    # z6_put_ok = False 

    # z7_get_ok = False
    # z7_put_ok = False  

    producing = False

