import logging
import asyncio

from asyncua import ua, Server
from asyncua.common.structures104 import new_struct, new_enum, new_struct_field

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger('asyncua')


async def main():
    # setup our server
    server = Server()
    await server.init()
    server.set_endpoint('opc.tcp://172.16.6.250:5616/')

    # setup our own namespace, not really necessary but should as spec
    uri = 'http://examples.freeopcua.github.io'
    idx = await server.register_namespace(uri)

    await new_struct(server, idx, "Order", [
        new_struct_field("orderNo", ua.VariantType.String),
        new_struct_field("productNo", ua.VariantType.String),
        new_struct_field("state", ua.VariantType.Int32),
        new_struct_field("duration", ua.VariantType.Float),
    ])

    await new_struct(server, idx, "AGV", [
        new_struct_field("orderNo", ua.VariantType.String),
        new_struct_field("position", ua.VariantType.Int32),
        new_struct_field("speed", ua.VariantType.Float, optional=True),
        new_struct_field("running", ua.VariantType.Int32),
    ])


    await server.load_data_type_definitions()

    order_1 = ua.Order()
    order_1.orderNo = 'PP000157'
    order_1.productNo = 'A01'
    order_1.state = 1
    order_1.duration = 35.6


    await server.nodes.objects.add_variable(idx, "order_1", ua.Variant(order_1, ua.VariantType.ExtensionObject))
    
    await server.nodes.objects.add_variable(idx, "order_2", ua.Variant(ua.Order(), ua.VariantType.ExtensionObject))
    await server.nodes.objects.add_variable(idx, "order_3", ua.Variant(ua.Order(), ua.VariantType.ExtensionObject))
    await server.nodes.objects.add_variable(idx, "order_4", ua.Variant(ua.Order(), ua.VariantType.ExtensionObject))
    await server.nodes.objects.add_variable(idx, "order_5", ua.Variant(ua.Order(), ua.VariantType.ExtensionObject))
    await server.nodes.objects.add_variable(idx, "order_6", ua.Variant(ua.Order(), ua.VariantType.ExtensionObject))
    await server.nodes.objects.add_variable(idx, "order_7", ua.Variant(ua.Order(), ua.VariantType.ExtensionObject))
    
    agv = ua.AGV()
    agv.orderNo = 'PP000157'
    agv.position = 5
    agv.speed = 9.99
    agv.running = 1

    await server.nodes.objects.add_variable(idx, "agv", ua.Variant(agv, ua.VariantType.ExtensionObject))

    async with server:
        while True:
            await asyncio.sleep(1)
            # new_val = await myvar.get_value() + 0.1
            # _logger.info('Set value of %s to %.1f', myvar, new_val)
            # await myvar.write_value(new_val)


if __name__ == '__main__':
    asyncio.run(main())