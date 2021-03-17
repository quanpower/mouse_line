#!/usr/bin/python
# -*- coding: utf-8 -*-

class gloVar():
    siemens_1500 = None
    plc_disconnected = False
    sockets = {}

    category = 'B'
    quantity = 0
    material_dict = []

    # system status
    camera_triggers = [0,0,0,0,0,0,0,0]
    robot_status = []
    wssArray = []
    
    pre_order_ok = False
    ready_ok = False
    warehouse_get_ok = False
    warehouse_put_ok = False
    line_get_ok_list = []
    line_put_ok_list = []
    plate_check_list = []
    producing_bool_get_ok_list = []
    work_done = False
    
    ua_order_list = []
    
    # 生产订单状态
    orderNo = ''
    productNo = ''
    state = 0
    startTime = 0


