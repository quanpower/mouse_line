import snap7
import threading
import time
import struct
from utils import int2bitarray
import ctypes

from snap7.common import check_error
from snap7.snap7types import S7DataItem, S7AreaDB, S7WLByte
import logging
logger = logging.getLogger(__name__)

class Siemens_s7(snap7.client.Client):
    def __init__(self):
        super().__init__()


    def write_bool_to_plc(self, dbNo, dbByte, index, value):
        logger.info('----write_bool_to_plc---')
        try:
            reading = self.db_read(dbNo, dbByte, 1)    # read 1 byte from db 31 staring from byte 120
            snap7.util.set_bool(reading, 0, index, value)   # set a value of fifth bit
            self.db_write(dbNo, dbByte, reading)    # write back the bytearray and now the boolean value is changed 
        except  Exception as e:
            logger.warning(e)
            logger.warning('write_bool_to_plc error')


    def write_byte_to_plc(self, dbNo, dbByte, value):
        logger.info('----write_byte_to_plc---')
        try:
            self.db_write(dbNo, dbByte, struct.pack('B', value))
            # self.write_area(0x84, dbNo, dbByte, struct.pack('B', value))
            # logger.info('=========write_byte_to_plc=========')
        except  Exception as e:
            logger.warning(e)
            logger.warning('write_byte_to_plc error')

    def write_int_to_plc(self, dbNo, dbByte, value):
        logger.info('----write_byte_to_plc---')
        try:
            self.db_write(dbNo, dbByte, struct.pack('>h', value))
            # self.write_area(0x84, dbNo, dbByte, struct.pack('B', value))
            # logger.info('=========write_byte_to_plc=========')
        except  Exception as e:
            logger.warning(e)
            logger.warning('write_byte_to_plc error')

    def write_real_to_plc(self, dbNo, dbByte, value):
        logger.info('----write_byte_to_plc---')
        try:
            x = struct.pack('>f', value)
            self.db_write(dbNo, dbByte, x)
            # self.write_area(0x84, dbNo, dbByte, struct.pack('B', value))
            # logger.info('=========write_byte_to_plc=========')
        except  Exception as e:
            logger.warning(e)
            logger.warning('write_byte_to_plc error')

    def read_bit_from_plc(self, dbNo, dbByte, index):
        try:
            return_byte = self.db_read(dbNo, dbByte, 1)
            bit_list = struct.unpack('1B', return_byte)
            return int2bitarray(bit_list, 8)
        except  Exception as e:
            logger.warning(e)
            logger.warning('read_bit_from_plc error')            


    def read_byte_from_plc(self, dbNo, dbByte):
        # logger.info('=========read_byte_from_plc=========')
        try:
            query_bitarray = self.db_read(dbNo, dbByte, 1)
            return struct.unpack('B', query_bitarray)[0]
        except  Exception as e:
            logger.warning(e)
            logger.warning('read_byte_from_plc error')   


    def read_16int_from_plc(self, dbNo, dbByte):
        # logger.info('=========read_16int_from_plc=========')              
        try:
            query_bitarray = self.db_read(dbNo, dbByte, 2)
            return_int = struct.unpack('H', query_bitarray)[0]
            return return_int
        except  Exception as e:
            logger.warning(e)
            logger.warning('read_16int_from_plc error') 


    def read_32int_from_plc(self, dbNo, dbByte):
        # logger.info('=========read_32int_from_plc=========')         
        try:
            query_bitarray = self.db_read(dbNo, dbByte, 4)
            return_int = struct.unpack('I', query_bitarray)[0]
            return return_int
        except  Exception as e:
            logger.warning(e)
            logger.warning('read_32int_from_plc error') 


    def query_block_from_plc(self, dbNo, dbByte, size):
        # logger.info('=========query_block_from_plc=========')        
        try:
            query_bitarray = self.db_read(dbNo, dbByte, size)
            return query_bitarray
        except  Exception as e:
            logger.warning(e)
            logger.warning('query_block_from_plc error') 


    def pulse_on(self, robot_addr, action):
        plc_addr = robot_addr[action]
        dbnumber = plc_addr['dbnumber']
        dbByte = plc_addr['byte']
        bit = plc_addr['bit']
        logger.info('----pulse_on----')
        self.write_bool_to_plc(dbnumber, dbByte, bit, 1)
        # time.sleep(5)
        # self.sendBitData(dbnumber, dbByte, bit, False)
        # 延迟断开


    def pulse_off(self, robot_addr, action):
        plc_addr = robot_addr[action]
        dbnumber = plc_addr['dbnumber']
        dbByte = plc_addr['byte']
        bit = plc_addr['bit']
        logger.info('----pulse_off----')
        self.write_bool_to_plc(dbnumber, dbByte, bit, 0)


    def send_data_to_plc(self, robot_addr, parameter, value):
        plc_addr = robot_addr[parameter]
        dbnumber = plc_addr['dbnumber']
        dbByte = plc_addr['byte']
        self.write_byte_to_plc(dbnumber, dbByte, value)


    def query_byte_from_plc(self, robot_addr, parameter):
        plc_addr = robot_addr[parameter]
        dbnumber = plc_addr['dbnumber']
        dbByte = plc_addr['byte']
        return self.read_byte_from_plc(dbnumber, dbByte)


    def query_16int_from_plc(self, robot_addr, parameter):
        plc_addr = robot_addr[parameter]
        dbnumber = plc_addr['dbnumber']
        dbByte = plc_addr['byte']
        return self.read_16int_from_plc(dbnumber, dbByte)


    def query_32int_from_plc(self, robot_addr, parameter):
        plc_addr = robot_addr[parameter]
        dbnumber = plc_addr['dbnumber']
        dbByte = plc_addr['byte']
        return self.read_32int_from_plc(dbnumber, dbByte)


    def query_multi_from_plc(self, dbNo):
        dbnumber = dbNo

        data_items = (S7DataItem * 3)()

        data_items[0].Area = ctypes.c_int32(S7AreaDB)
        data_items[0].WordLen = ctypes.c_int32(S7WLByte)
        data_items[0].Result = ctypes.c_int32(0)
        data_items[0].DBNumber = ctypes.c_int32(dbnumber)
        data_items[0].Start = ctypes.c_int32(0)
        data_items[0].Amount = ctypes.c_int32(4)  # reading a REAL, 4 bytes

        data_items[1].Area = ctypes.c_int32(S7AreaDB)
        data_items[1].WordLen = ctypes.c_int32(S7WLByte)
        data_items[1].Result = ctypes.c_int32(0)
        data_items[1].DBNumber = ctypes.c_int32(dbnumber)
        data_items[1].Start = ctypes.c_int32(12)
        data_items[1].Amount = ctypes.c_int32(4)  # reading a REAL, 4 bytes

        data_items[2].Area = ctypes.c_int32(S7AreaDB)
        data_items[2].WordLen = ctypes.c_int32(S7WLByte)
        data_items[2].Result = ctypes.c_int32(0)
        data_items[2].DBNumber = ctypes.c_int32(dbnumber)
        data_items[2].Start = ctypes.c_int32(2)
        data_items[2].Amount = ctypes.c_int32(2)  # reading an INT, 2 bytes

        # create buffers to receive the data
        # use the Amount attribute on each item to size the buffer
        for di in data_items:
            # create the buffer
            buffer = ctypes.create_string_buffer(di.Amount)

            # cast the pointer to the buffer to the required type
            pBuffer = ctypes.cast(ctypes.pointer(buffer),
                                  ctypes.POINTER(ctypes.c_uint8))
            di.pData = pBuffer

        result, data_items = self.read_multi_vars(data_items)

        for di in data_items:
            check_error(di.Result)

        result_values = []

        # function to cast bytes to match data_types[] above
        byte_to_value = [snap7.util.get_int, snap7.util.get_int, snap7.util.get_int]

        # unpack and test the result of each read
        for i in range(0, len(data_items)):
            btv = byte_to_value[i]
            di = data_items[i]
            value = btv(di.pData, 0)
            result_values.append(value)
        logger.info(result_values)

