import logging
import asyncio
import sys
sys.path.insert(0, "..")

from asyncua import ua, Server
from asyncua.common.methods import uamethod


logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger('asyncua')


@uamethod
def func(parent, value):
    return value * 2


async def main():
    # setup our server
    server = Server()
    await server.init()

    server.set_endpoint('opc.tcp://172.16.6.250:5616/')
    # server.set_endpoint('opc.tcp://192.168.1.8:5616/')
    server.set_server_name("AGV OpcUa Server")
    # # setup our own namespace, not really necessary but should as spec
    uri = 'http://examples.freeopcua.github.io'
    idx = await server.register_namespace(uri)

    # populating our address space
    # server.nodes, contains links to very common nodes like objects and root

    order_folder = await server.nodes.objects.add_folder(idx, "orderFolder")

    order_1 = await order_folder.add_object(idx, 'order_1')
    order_1_orderNo = await order_1.add_variable(idx, 'orderNo', 'PP000151')
    order_1_productNo = await order_1.add_variable(idx, 'productNo', 'A01')
    order_1_state = await order_1.add_variable(idx, 'state', 0)
    order_1_duration = await order_1.add_variable(idx, 'duration', 6.7)

    order_2 = await order_folder.add_object(idx, 'order_2')
    order_2_orderNo = await order_2.add_variable(idx, 'orderNo', 'PP000151')
    order_2_productNo = await order_2.add_variable(idx, 'productNo', 'A01')
    order_2_state = await order_2.add_variable(idx, 'state', 0)
    order_2_duration = await order_2.add_variable(idx, 'duration', 6.7)

    order_3 = await order_folder.add_object(idx, 'order_3')
    order_3_orderNo = await order_3.add_variable(idx, 'orderNo', 'PP000151')
    order_3_productNo = await order_3.add_variable(idx, 'productNo', 'A01')
    order_3_state = await order_3.add_variable(idx, 'state', 0)
    order_3_duration = await order_3.add_variable(idx, 'duration', 6.7)

    order_4 = await order_folder.add_object(idx, 'order_4')
    order_4_orderNo = await order_4.add_variable(idx, 'orderNo', 'PP000151')
    order_4_productNo = await order_4.add_variable(idx, 'productNo', 'A01')
    order_4_state = await order_4.add_variable(idx, 'state', 0)
    order_4_duration = await order_4.add_variable(idx, 'duration', 6.7)

    order_5 = await order_folder.add_object(idx, 'order_5')
    order_5_orderNo = await order_5.add_variable(idx, 'orderNo', 'PP000151')
    order_5_productNo = await order_5.add_variable(idx, 'productNo', 'A01')
    order_5_state = await order_5.add_variable(idx, 'state', 0)
    order_5_duration = await order_5.add_variable(idx, 'duration', 6.7)

    order_6 = await order_folder.add_object(idx, 'order_6')
    order_6_orderNo = await order_6.add_variable(idx, 'orderNo', 'PP000151')
    order_6_productNo = await order_6.add_variable(idx, 'productNo', 'A01')
    order_6_state = await order_6.add_variable(idx, 'state', 0)
    order_6_duration = await order_6.add_variable(idx, 'duration', 6.7)

    order_7 = await order_folder.add_object(idx, 'order_7')
    order_7_orderNo = await order_7.add_variable(idx, 'orderNo', 'PP000151')
    order_7_productNo = await order_7.add_variable(idx, 'productNo', 'A01')
    order_7_state = await order_7.add_variable(idx, 'state', 0)
    order_7_duration = await order_7.add_variable(idx, 'duration', 6.7)

    agv_order = await order_folder.add_object(idx, 'agv_order')
    agv_orderNo = await agv_order.add_variable(idx, 'agv_order_list', 'PP000151,PP000152,PP000153')

    agv_folder = await server.nodes.objects.add_folder(idx, "agvFolder")

    agv = await agv_folder.add_object(idx, 'agv')

    position = await agv.add_variable(idx, 'position', '5')
    speed = await agv.add_variable(idx, 'speed', 9.99)
    running = await agv.add_variable(idx, 'running', 1)


    # Set MyVariable to be writable by clients
    await position.set_writable()
    await speed.set_writable()
    await running.set_writable()

    # await server.nodes.objects.add_method(ua.NodeId('ServerMethod', 2), ua.QualifiedName('ServerMethod', 2), func, [ua.VariantType.Int64], [ua.VariantType.Int64])
    
    _logger.info('Starting server!')
    async with server:
        while True:
            await asyncio.sleep(1)
            new_val = await order_1_duration.get_value() + 0.1
            _logger.info('Set value of %s to %.1f', order_1_duration, new_val)
            await order_1_duration.write_value(new_val)
            await order_2_duration.write_value(new_val)
            await order_3_duration.write_value(new_val)
            await order_4_duration.write_value(new_val)
            await order_5_duration.write_value(new_val)
            await order_6_duration.write_value(new_val)
            await order_7_duration.write_value(new_val)


if __name__ == '__main__':
    asyncio.run(main())