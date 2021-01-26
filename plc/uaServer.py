import logging
import datetime
import time
from global_list import gloVar
import sys
sys.path.insert(0, "..")

# logger = logging.getLogger(__name__)
logger = logging.getLogger('uaServer')

from opcua import ua, Server

def ua_main():
    # setup our server
    server = Server()
    server.set_endpoint("opc.tcp://172.16.6.250:5616/")

    # setup our own namespace, not really necessary but should as spec
    uri = "http://examples.freeopcua.github.io"
    idx = server.register_namespace(uri)

    # get Objects node, this is where we should put our nodes
    objects = server.get_objects_node()

    # # populating our address space
    # myobj = objects.add_object(idx, "MyObject")
    # myvar = myobj.add_variable(idx, "MyVariable", 6.7)
    # myvar.set_writable()    # Set MyVariable to be writable by clients

    order_folder =  server.nodes.objects.add_folder(idx, "orderFolder")

    order_1 =  order_folder.add_object(idx, 'order_1')
    order_1_orderNo =  order_1.add_variable(idx, 'orderNo', 'PP000151')
    order_1_productNo =  order_1.add_variable(idx, 'productNo', 'A01')
    order_1_state =  order_1.add_variable(idx, 'state', 0)
    order_1_duration =  order_1.add_variable(idx, 'duration', 0)

    order_2 =  order_folder.add_object(idx, 'order_2')
    order_2_orderNo =  order_2.add_variable(idx, 'orderNo', 'PP000000')
    order_2_productNo =  order_2.add_variable(idx, 'productNo', 'A01')
    order_2_state =  order_2.add_variable(idx, 'state', 0)
    order_2_duration =  order_2.add_variable(idx, 'duration', 0)

    order_3 =  order_folder.add_object(idx, 'order_3')
    order_3_orderNo =  order_3.add_variable(idx, 'orderNo', 'PP000000')
    order_3_productNo =  order_3.add_variable(idx, 'productNo', 'A01')
    order_3_state =  order_3.add_variable(idx, 'state', 0)
    order_3_duration =  order_3.add_variable(idx, 'duration', 0)

    order_4 =  order_folder.add_object(idx, 'order_4')
    order_4_orderNo =  order_4.add_variable(idx, 'orderNo', 'PP000000')
    order_4_productNo =  order_4.add_variable(idx, 'productNo', 'A01')
    order_4_state =  order_4.add_variable(idx, 'state', 0)
    order_4_duration =  order_4.add_variable(idx, 'duration', 0)

    order_5 =  order_folder.add_object(idx, 'order_5')
    order_5_orderNo =  order_5.add_variable(idx, 'orderNo', 'PP000000')
    order_5_productNo =  order_5.add_variable(idx, 'productNo', 'A01')
    order_5_state =  order_5.add_variable(idx, 'state', 0)
    order_5_duration =  order_5.add_variable(idx, 'duration', 0)

    order_6 =  order_folder.add_object(idx, 'order_6')
    order_6_orderNo =  order_6.add_variable(idx, 'orderNo', 'PP000000')
    order_6_productNo =  order_6.add_variable(idx, 'productNo', 'A01')
    order_6_state =  order_6.add_variable(idx, 'state', 0)
    order_6_duration =  order_6.add_variable(idx, 'duration', 0)

    order_7 =  order_folder.add_object(idx, 'order_7')
    order_7_orderNo =  order_7.add_variable(idx, 'orderNo', 'PP000000')
    order_7_productNo =  order_7.add_variable(idx, 'productNo', 'A01')
    order_7_state =  order_7.add_variable(idx, 'state', 0)
    order_7_duration =  order_7.add_variable(idx, 'duration', 0)

    agv_order =  order_folder.add_object(idx, 'agv_order')
    agv_orderNo =  agv_order.add_variable(idx, 'agv_order_list', 'PP000151,PP000152,PP000153')

    agv_folder =  server.nodes.objects.add_folder(idx, "agvFolder")

    agv =  agv_folder.add_object(idx, 'agv')

    position =  agv.add_variable(idx, 'position', '5')
    speed =  agv.add_variable(idx, 'speed', 9.99)
    running =  agv.add_variable(idx, 'running', 1)

    # Set MyVariable to be writable by clients

    position.set_writable()
    speed.set_writable()
    running.set_writable()


    # starting!
    server.start()

    try:
        while True:
            time.sleep(0.5)

            duration = time.time() - gloVar.startTime
            # logger.info('Set value of %s to %.1f', order_1_duration, duration)
            order_1_orderNo.set_value(gloVar.orderNo)
            order_1_productNo.set_value(gloVar.productNo)
            order_1_state.set_value(gloVar.state)
            order_1_duration.set_value(duration)
    finally:
        #close connection, remove subcsriptions, etc
        server.stop()

if __name__ == "__main__":        
    ua_main()