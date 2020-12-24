robots_addr = {
    'robot_0': {
        # -----------PC---->PLC----------------
        #
        # DB1.DBX0.0
        'sys_reset_addr': {
            'area': 0x84,
            'dbnumber': 1,
            'byte': 0,
            'bit':0,
        },

        # DB1.DBX0.1
        'err_reset_addr': {
            'area': 0x84,
            'dbnumber': 1,
            'byte': 0,
            'bit':1,
        },
        
        # DB1.DBX0.2
        'in_enable_addr': {
            'area': 0x84,
            'dbnumber': 1,
            'byte': 0,
            'bit':2,
        },

        # DB1.DBX0.3
        'out_enable_addr': {
            'area': 0x84,
            'dbnumber': 1,
            'byte': 0,
            'bit':3,
        },
      
        # DB1.DBX0.4
        'move_enable_addr': {
            'area': 0x84,
            'dbnumber': 1,
            'byte': 0,
            'bit':4,
        },
              
        # DB1.DBX0.5
        'redo_input_enable_addr': {
            'area': 0x84,
            'dbnumber': 1,
            'byte': 0,
            'bit':5,
        },

        # DB1.DBX0.6
        'move_emergency_addr': {
            'area': 0x84,
            'dbnumber': 1,
            'byte': 0,
            'bit':6,
        },
        # DB1.DBX1.0
        'camera_enable_addr': {
            'area': 0x84,
            'dbnumber': 1,
            'byte': 1,
            'bit':0,
        },

        # DB1.DBX1.1
        'camera_back_addr': {
            'area': 0x84,
            'dbnumber': 1,
            'byte': 1,
            'bit':1,
        },

        # DB1.DBX1.2
        'camera_clear_addr': {
            'area': 0x84,
            'dbnumber': 1,
            'byte': 1,
            'bit':2,
        },

        # DB1.DBX1.3
        'camera_data_ok_addr': {
            'area': 0x84,
            'dbnumber': 1,
            'byte': 1,
            'bit':3,
        },

        # DB1.DBB10
        'in_position_addr': {
            'area': 0x84,
            'dbnumber': 1,
            'byte': 10,
            'bit':0,
        },

        # DB1.DBB11
        'out_position_addr': {
            'area': 0x84,
            'dbnumber': 1,
            'byte': 11,
            'bit':0,
        },

        # DB1.DBB12
        'move_src_position_addr': {
            'area': 0x84,
            'dbnumber': 1,
            'byte': 12,
            'bit':0,
        },

        # DB1.DBB13
        'move_dst_position_addr': {
            'area': 0x84,
            'dbnumber': 1,
            'byte': 13,
            'bit':0,
        },

        # DB1.DBB14
        'redo_position_addr': {
            'area': 0x84,
            'dbnumber': 1,
            'byte': 14,
            'bit':0,
        },

        # DB1.DBB20
        'in_battery_position_seq_addr': {
            'area': 0x84,
            'dbnumber': 1,
            'byte': 20,
            'bit':0,
        },

        # DB1.DBB21
        'out_battery_position_seq_addr': {
            'area': 0x84,
            'dbnumber': 1,
            'byte': 21,
            'bit':0,
        },



        # -----------PLC---->PC----------------

        # DB1.DBX5.0
        'in_request_addr': {
            'area': 0x84,
            'dbnumber': 1,
            'byte': 5,
            'bit':0,
        },

         # DB1.DBX5.1
        'out_request_addr': {
            'area': 0x84,
            'dbnumber': 1,
            'byte': 5,
            'bit':1,
        },

     
         # DB1.DBX5.2
        'loading_flag_addr': {
            'area': 0x84,
            'dbnumber': 1,
            'byte': 5,
            'bit':2,
        },


         # DB1.DBX5.3
        'blanking_flag_addr': {
            'area': 0x84,
            'dbnumber': 1,
            'byte': 5,
            'bit':3,
        },

        # DB1.DBX5.4
        'system_reset_done_addr': {
            'area': 0x84,
            'dbnumber': 1,
            'byte': 5,
            'bit':4,
        },

         # DB1.DBB30
        'work_mode_addr': {
            'area': 0x84,
            'dbnumber': 1,
            'byte': 30,
            'bit':0,
        },


         # DB1.DBB31
        'robot_state_addr': {
            'area': 0x84,
            'dbnumber': 1,
            'byte': 31,
            'bit':0,
        },


         # DB1.DBB32
        'robot_position_addr': {
            'area': 0x84,
            'dbnumber': 1,
            'byte': 32,
            'bit':0,
        },


         # DB1.DBB33
        'battery_need_replace_addr': {
            'area': 0x84,
            'dbnumber': 1,
            'byte': 33,
            'bit':0,
        },


         # DB1.DBI40
        'robot_error_addr': {
            'area': 0x84,
            'dbnumber': 1,
            'byte': 40,
            'bit':0,
        },


         # DB1.DBI42
        'jig_error_addr': {
            'area': 0x84,
            'dbnumber': 1,
            'byte': 42,
            'bit':0,
        },


         # DB1.DBI44
        'servo_error_addr': {
            'area': 0x84,
            'dbnumber': 1,
            'byte': 44,
            'bit':0,
        },

         # DB1.DBW46
        'cart_error_addr': {
            'area': 0x84,
            'dbnumber': 1,
            'byte': 46,
            'bit':0,
        },
################共用####################
         # DB1.DBI50
        'PLC_error_addr': {
            'area': 0x84,
            'dbnumber': 1,
            'byte': 50,
            'bit':0,
        },

         # DB1.DBI52
        'left_car_status_addr': {
            'area': 0x84,
            'dbnumber': 1,
            'byte': 52,
            'bit':0,
        },

         # DB1.DBI53
        'right_car_status_addr': {
            'area': 0x84,
            'dbnumber': 1,
            'byte': 52,
            'bit':0,
        },

         # DB1.DBB49
        'net_error_addr': {
            'area': 0x84,
            'dbnumber': 1,
            'byte': 54,
            'bit':0,
        },

    },
    
    'robot_1': {
        # -----------PC---->PLC----------------
        #
        # DB2.DBX0.0
        'sys_reset_addr': {
            'area': 0x84,
            'dbnumber': 2,
            'byte': 0,
            'bit':0,
        },

        # DB2.DBX0.1
        'err_reset_addr': {
            'area': 0x84,
            'dbnumber': 2,
            'byte': 0,
            'bit':1,
        },
        
        # DB2.DBX0.2
        'in_enable_addr': {
            'area': 0x84,
            'dbnumber': 2,
            'byte': 0,
            'bit':2,
        },

        # DB2.DBX0.3
        'out_enable_addr': {
            'area': 0x84,
            'dbnumber': 2,
            'byte': 0,
            'bit':3,
        },
     
        # DB2.DBX0.4
        'move_enable_addr': {
            'area': 0x84,
            'dbnumber': 2,
            'byte': 0,
            'bit':4,
        },
              
        # DB2.DBX0.5
        'redo_input_enable_addr': {
            'area': 0x84,
            'dbnumber': 2,
            'byte': 0,
            'bit':5,
        },

        # DB2.DBX0.6
        'move_emergency_addr': {
            'area': 0x84,
            'dbnumber': 2,
            'byte': 0,
            'bit':6,
        },
        # DB2.DBX1.0
        'camera_enable_addr': {
            'area': 0x84,
            'dbnumber': 2,
            'byte': 1,
            'bit':0,
        },

        # DB2.DBX1.1
        'camera_back_addr': {
            'area': 0x84,
            'dbnumber': 2,
            'byte': 1,
            'bit':1,
        },

        # DB2.DBX1.2
        'camera_clear_addr': {
            'area': 0x84,
            'dbnumber': 2,
            'byte': 1,
            'bit':2,
        },

        # DB2.DBX1.3
        'camera_data_ok_addr': {
            'area': 0x84,
            'dbnumber': 2,
            'byte': 1,
            'bit':3,
        },

        # DB2.DBB10
        'in_position_addr': {
            'area': 0x84,
            'dbnumber': 2,
            'byte': 10,
            'bit':0,
        },

        # DB2.DBB11
        'out_position_addr': {
            'area': 0x84,
            'dbnumber': 2,
            'byte': 11,
            'bit':0,
        },

        # DB2.DBB12
        'move_src_position_addr': {
            'area': 0x84,
            'dbnumber': 2,
            'byte': 12,
            'bit':0,
        },

        # DB2.DBB13
        'move_dst_position_addr': {
            'area': 0x84,
            'dbnumber': 2,
            'byte': 13,
            'bit':0,
        },

        # DB2.DBB14
        'redo_position_addr': {
            'area': 0x84,
            'dbnumber': 2,
            'byte': 14,
            'bit':0,
        },

        # DB2.DBB20
        'in_battery_position_seq_addr': {
            'area': 0x84,
            'dbnumber': 2,
            'byte': 20,
            'bit':0,
        },

        # DB2.DBB21
        'out_battery_position_seq_addr': {
            'area': 0x84,
            'dbnumber': 2,
            'byte': 21,
            'bit':0,
        },

        # -----------PLC---->PC----------------

        # DB2.DBX5.0
        'in_request_addr': {
            'area': 0x84,
            'dbnumber': 2,
            'byte': 5,
            'bit':0,
        },

         # DB2.DBX5.1
        'out_request_addr': {
            'area': 0x84,
            'dbnumber': 2,
            'byte': 5,
            'bit':1,
        },

         # DB2.DBX5.2
        'loading_flag_addr': {
            'area': 0x84,
            'dbnumber': 2,
            'byte': 5,
            'bit':2,
        },

         # DB2.DBX5.3
        'blanking_flag_addr': {
            'area': 0x84,
            'dbnumber': 2,
            'byte': 5,
            'bit':3,
        },

        # DB2.DBX5.4
        'system_reset_done_addr': {
            'area': 0x84,
            'dbnumber': 2,
            'byte': 5,
            'bit':4,
        },

         # DB2.DBB30
        'work_mode_addr': {
            'area': 0x84,
            'dbnumber': 2,
            'byte': 30,
            'bit':0,
        },

         # DB2.DBB31
        'robot_state_addr': {
            'area': 0x84,
            'dbnumber': 2,
            'byte': 31,
            'bit':0,
        },

         # DB2.DBB32
        'robot_position_addr': {
            'area': 0x84,
            'dbnumber': 2,
            'byte': 32,
            'bit':0,
        },

         # DB2.DBB33
        'battery_need_replace_addr': {
            'area': 0x84,
            'dbnumber': 2,
            'byte': 33,
            'bit':0,
        },

         # DB2.DBW40
        'robot_error_addr': {
            'area': 0x84,
            'dbnumber': 2,
            'byte': 40,
            'bit':0,
        },

         # DB2.DBW41
        'jig_error_addr': {
            'area': 0x84,
            'dbnumber': 2,
            'byte': 42,
            'bit':0,
        },

         # DB2.DBW42
        'servo_error_addr': {
            'area': 0x84,
            'dbnumber': 2,
            'byte': 44,
            'bit':0,
        },
################共用####################
         # DB2.DBW50
        'PLC_error_addr': {
            'area': 0x84,
            'dbnumber': 1,
            'byte': 50,
            'bit':0,
        },

         # DB2.DBW51
        'left_car_status_addr': {
            'area': 0x84,
            'dbnumber': 1,
            'byte': 52,
            'bit':0,
        },

         # DB1.DBW52
        'right_car_status_addr': {
            'area': 0x84,
            'dbnumber': 1,
            'byte': 53,
            'bit':0,
        },

        # DB1.DBW54
        'net_error_addr': {
            'area': 0x84,
            'dbnumber': 1,
            'byte': 54,
            'bit':0,
        },

    },

}