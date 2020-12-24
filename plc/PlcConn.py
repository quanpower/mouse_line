from SiemensClassLock import Siemens_s7
import time
import threading
from global_list import gloVar
import logging

logger = logging.getLogger(__name__)

PLC_IP = '172.16.6.200'
RACK = 0
SLOT = 1

def plcConn():
    siemens_1500 = Siemens_s7()
    while True:
        try:
            logger.info('---reconnecting...----')
            gloVar.plc_disconnected = False
            siemens_1500.connect(PLC_IP, RACK, SLOT)
            logger.info('---siemens_1500 connected----')
            gloVar.siemens_1500 = siemens_1500

            logger.info(str(siemens_1500.get_cpu_state()))
            # while str(siemens_1500.get_cpu_state())== "S7CpuStatusRun":
            while siemens_1500.get_connected():
                time.sleep(1)
                if gloVar.plc_disconnected:
                    logger.info('plc disconned......')
                    break
            logger.info("---siemens_1500 disconnected,reconnecting...-----")

            siemens_1500.disconnect()
            # siemens_1500.destroy()
            time.sleep(0.5)
        except  Exception as e:
            logger.info('\n' *3 )
            logger.info('=====siemens_1500 connect error!====')
            logger.info(e)
            # siemens_1500 = Siemens_s7()
        time.sleep(1)

