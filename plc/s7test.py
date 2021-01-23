import snap7
from snap7.util import *
from snap7.snap7types import *
import struct

s1500=snap7.client.Client()
s1500.connect('172.16.6.200',rack=0,slot=1)
Real_Value=s1500.read_area(0x84,38,0,1)
print(Real_Value)

order = '00PP000022'
byarray=bytearray(order,encoding='utf-8')

print(byarray)

productNo = '00A03'
productNobyarray=bytearray(productNo,encoding='utf-8')


for i, val in enumerate(byarray):
    index = 98 + i 
    print ("序号：%s   值：%s" % (i + 1, val))
    s1500.write_area(0x84,38,index, struct.pack('B', val))

for i, val in enumerate(productNobyarray):
    index = 354 + i 
    print ("序号：%s   值：%s" % (i + 1, val))
    s1500.write_area(0x84,38,index, struct.pack('B', val))

Real_Value=s1500.read_area(0x84,38,98,15)
print(Real_Value)

Real_Value=s1500.read_area(0x84,38,354,15)
print(Real_Value)