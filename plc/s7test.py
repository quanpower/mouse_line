import snap7
from snap7.util import *
from snap7.snap7types import *
s1500=snap7.client.Client()
s1500.connect('192.168.0.20',rack=0,slot=1)
Real_Value=s1500.read_area(0x84,38,0,1)
print(Real_Value)