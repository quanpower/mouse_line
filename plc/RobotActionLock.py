import threading
import time
import datetime
import struct
from plc_addr import robots_addr
from utils import int2bitarray

from global_list import gloVar

import logging
logger = logging.getLogger(__name__)


def dont_do_anything():
    pass


def in_action(siemens_1500, positionByte, position, enableByte, enableBit, enable, glock):
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


def out_action(siemens_1500, positionByte, enableByte, enableBit, enable, out_list, glock):
    logger.info('---out action----start-----')
    print('---out action----start-----')
    print(out_list)
    for position in out_list:
        i = 0
        while 1: 
            print(datetime.datetime.now())

            if gloVar.ready_ok:
                print('=====output no=====')
                print(position)
                with glock:
                    siemens_1500.write_int_to_plc(38, positionByte, position)
                    time.sleep(0.1)
                    siemens_1500.write_bool_to_plc(38, enableByte, enableBit, enable)
                    print(positionByte)
                    print(enableByte)
                    print(enableBit)
                    print(enable)

                time.sleep(10)

                # 出库使能复位
                with glock:
                    siemens_1500.write_bool_to_plc(38, enableByte, enableBit, 0)
                logger.info(position)
                break

            i += 1
            print(i)
            # 跳出while,结束出库
            if i >= 600:
                return
            time.sleep(1)

    logger.info('---out action---end-------')
    print('---out action---end-------')
