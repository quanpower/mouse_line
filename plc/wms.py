from typing import List

import databases
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel
import datetime
import uvicorn
import json
from typing import Optional
import requests

from utils import generate_materials_list, generate_plate_info_json, generate_warehouse_info, \
    generate_warehouse_info_init, generate_line_storage_info, \
    generate_line_storage_info_init, generate_material_storage_init, get_material_dict, generate_material_list_json

app = FastAPI()

# SQLAlchemy specific code, as with any other app
DATABASE_URL = "sqlite:///./wms.db"
# DATABASE_URL = "postgresql://user:password@postgresserver/db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()


materials = sqlalchemy.Table(
    "materials",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("materialCode", sqlalchemy.String(10)),
    sqlalchemy.Column("materialName", sqlalchemy.String(20)),
    sqlalchemy.Column("materialClass", sqlalchemy.String(10)),
    sqlalchemy.Column("description", sqlalchemy.String(50)),
)

warehouse = sqlalchemy.Table(
    "warehouse",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("locatorCode", sqlalchemy.String(10)),
    sqlalchemy.Column("isEmpty", sqlalchemy.Boolean),
    sqlalchemy.Column("materialList", sqlalchemy.Text),
)

linestorage = sqlalchemy.Table(
    "linestorage",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("lineStorageCode", sqlalchemy.String(20)),
    sqlalchemy.Column("isEmpty", sqlalchemy.Boolean),
    sqlalchemy.Column("materialList", sqlalchemy.Text),
    sqlalchemy.Column("source", sqlalchemy.Integer),
)

material_storage = sqlalchemy.Table(
    "material_storage",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("materialCode", sqlalchemy.String(10)),
    sqlalchemy.Column("locatorCode", sqlalchemy.Text),
)

plateinfo = sqlalchemy.Table(
    "plateinfo",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("plateName", sqlalchemy.String(10)),
    sqlalchemy.Column("plateClass", sqlalchemy.String(10)),
    sqlalchemy.Column("length", sqlalchemy.Integer),
    sqlalchemy.Column("width", sqlalchemy.Integer),
)

warehouse_version = sqlalchemy.Table(
    "warehouse_version",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, autoincrement=True,primary_key=True),
    sqlalchemy.Column("created_date", sqlalchemy.DateTime, default=datetime.datetime.utcnow()),
)

linestorage_version = sqlalchemy.Table(
    "linestorage_version",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, autoincrement=True,primary_key=True),
    sqlalchemy.Column("created_date", sqlalchemy.DateTime, default=datetime.datetime.utcnow()),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)


class OrderDetail(BaseModel):
    seq: str
    customerCode: str
    customerName: str
    productCode: str
    productName: str
    signType: int
    signValue: str
    materialList: list = []

class Order(BaseModel):
    orders: list = []

class WHPlate(BaseModel):
    isEmpty: bool
    materialList: str
    
class LSPlate(BaseModel):
    isEmpty: bool
    materialList: str
    source: int
    

def get_material_code(material_dict, position):
    for key,value in material_dict.items():
        if str(position) in value:
            return key


@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# 初始化数据库列表
@app.post("/v1/api/wms/materials/init")
async def materials_init():
    query = materials.insert().values(generate_materials_list())
    last_record_id = await database.execute(query)

    return {
        "code" : 0,
        "message" : "数据处理成功！",
        "data" : {"id": last_record_id}
    }

@app.post("/v1/api/wms/warehouse/init")
async def warehouse_init():
    query = warehouse.insert().values(generate_warehouse_info_init())
    last_record_id = await database.execute(query)

    return {
        "code" : 0,
        "message" : "数据处理成功！",
        "data" : {"id": last_record_id}
    }

@app.post("/v1/api/wms/line_storage/init")
async def line_storage_init():
    query = linestorage.insert().values(generate_line_storage_info_init())
    last_record_id = await database.execute(query)

    return {
        "code" : 0,
        "message" : "数据处理成功！",
        "data" : {"id": last_record_id}
    }

@app.post("/v1/api/wms/material_storage/init")
async def material_storage_init():
    query = material_storage.insert().values(generate_material_storage_init())
    last_record_id = await database.execute(query)

    return {
        "code" : 0,
        "message" : "数据处理成功！",
        "data" : {"id": last_record_id}
    }

# 物料对应储位列表
@app.get("/v1/api/wms/material_storage")
async def get_material_storage():
    query = material_storage.select()
    result = await database.fetch_all(query)

    return {
        "code" : 0,
        "message" : "数据处理成功！",
        "data" : result
    }


# 立库储位，版本
@app.get("/v1/api/wms/warehouse/snapshot/list")
async def get_warehouse_snapshot(ver: Optional[int] = None):
    ver_query = warehouse_version.select().order_by(warehouse_version.c.id.desc())
    version = await database.fetch_one(ver_query)

    query = warehouse.select()
    result = await database.fetch_all(query)
    snapshot = []
    for i in result:
        materialList_dict = json.loads(i.materialList)
        materialList = []
        for key,value in materialList_dict.items():
            plate = {}
            plate['materialPlace'] = key
            plate['materialCode'] = value
            materialList.append(plate)
        snapshot.append({"locatorCode": i.locatorCode, "materialList": materialList})

    outandin = [
                {
                    "action":"out",
                    "locatorCode":"021",
                    "materialList":[
                        {
                            "materialCode":"Ba01.01",
                            "materialPlace":"3"
                        },
                    ],
                }
            ]

    return_json = {
        "code" : 0,
        "message" : "数据处理成功！",
        "data" : {
            "ver":version.id,
            "snapshot":snapshot,
            "outandin":outandin
        }
    }
    return return_json

"""

            "outandin":[
                {
                    "action":"out",
                    "locatorCode":"021",
                    "materialList":[
                        {
                            "materialCode":"Ba01.01",
                            "materialPlace":"3"
                        },
                    ],
                }
            ]

"""

@app.get("/v1/api/wms/warehouse/bin/{bin_id}")
async def get_warehouse_bin(bin_id: int, q: Optional[str] = None):
    query = warehouse.select().where(warehouse.c.id==bin_id)
    result = await database.fetch_all(query)

    return_json = {
        "code" : 0,
        "message" : "数据处理成功！",
        "data" : result
    }
    return return_json

@app.put("/v1/api/wms/warehouse/bin/{bin_id}")
async def update_warehouse_bin(bin_id: int, plate: WHPlate, q: Optional[str] = None):
    # materialList = generate_plate_info_json(1,10,'Za01.01') 
    isEmpty = plate.isEmpty
    materialList = plate.materialList
    print(materialList)
    query = warehouse.update().where(warehouse.c.id==bin_id).values(isEmpty=isEmpty, materialList=materialList)
    last_record_id = await database.execute(query)

    return_json = {
        "code" : 0,
        "message" : "数据处理成功！",
        "data" : {"id": last_record_id, "bin_id": bin_id}
    }
    return return_json


@app.post("/v1/api/wms/warehouse/version")
async def create_warehouse_version():
    query = warehouse_version.insert().values(created_date=datetime.datetime.now())
    last_record_id = await database.execute(query)

    return {
        "code" : 0,
        "message" : "数据处理成功！",
        "data" : {"id": last_record_id}
    }

@app.get("/v1/api/wms/warehouse/version")
async def get_warehouse_version():
    query = warehouse_version.select()
    result = await database.fetch_all(query)

    return {
        "code" : 0,
        "message" : "数据处理成功！",
        "data" : result
    }

# 线边库储位，版本
@app.get("/v1/api/wms/line_storage/snapshot/list")
async def get_line_storage_snapshot(ver: Optional[int] = None):
    ver_query = linestorage_version.select().order_by(linestorage_version.c.id.desc())
    version = await database.fetch_one(ver_query)

    query = linestorage.select()
    result = await database.fetch_all(query)
    snapshot = []
    for i in result:
        materialList_dict = json.loads(i.materialList)
        materialList = []
        for key,value in materialList_dict.items():
            plate = {}
            plate['materialPlace'] = key
            plate['materialCode'] = value
            materialList.append(plate)
        snapshot.append({"lineStorageCode": i.lineStorageCode, "materialList": materialList})

    outandin = [
                    {
                        "action":"in",
                        "lineStorageCode":"LineStorage3",
                        "materialList":[
                            {
                                "materialCode":"Ba01.01",
                                "materialPlace":"3"
                            },
                        ]
                    }
                ]
    return_json = {
        "code" : 0,
        "message" : "数据处理成功！",
        "data" : {
            "ver": version.id,
            "snapshot": snapshot,
            "outandin": outandin 
        }
    }
    return return_json

    """
                    "outandin":[
                    {
                        "action":"in",
                        "lineStorageCode":"LineStorage3",
                        "materialList":[
                            {
                                "materialCode":"Ba01.01",
                                "materialPlace":"3"
                            },
                        ]
                    }
                ],

    """

@app.get("/v1/api/wms/line_storage/bin/{bin_id}")
async def get_line_storage_bin(bin_id: int, q: Optional[str] = None):

    query = linestorage.select().where(linestorage.c.id==bin_id)
    result = await database.fetch_all(query)

    return_json = {
        "code" : 0,
        "message" : "数据处理成功！",
        "data" : result
    }
    return return_json

@app.put("/v1/api/wms/line_storage/bin/{bin_id}")
async def update_line_storage_bin(bin_id: int, plate: LSPlate, q: Optional[str] = None):
    isEmpty = plate.isEmpty
    materialList = plate.materialList
    source = plate.source 
    print(materialList)
    query = linestorage.update().where(linestorage.c.id==bin_id).values(isEmpty=isEmpty, materialList=materialList, source=source)
    last_record_id = await database.execute(query)

    return_json = {
        "code" : 0,
        "message" : "数据处理成功！",
        "data" : {"id": last_record_id, "bin_id": bin_id}
    }
    return return_json

@app.post("/v1/api/wms/line_storage/version")
async def create_line_storage_version():
    query = linestorage_version.insert().values(created_date=datetime.datetime.now())
    last_record_id = await database.execute(query)
    return {
        "code" : 0,
        "message" : "数据处理成功！",
        "data" : {"id": last_record_id}
    }

@app.get("/v1/api/wms/line_storage/version")
async def get_line_storage_version():
    query = linestorage_version.select()
    result = await database.fetch_all(query)
    return {
        "code" : 0,
        "message" : "数据处理成功！",
        "data" : result
    }

# 生产订单列表
@app.put("/v1/api/order/produce/list")
async def update_order_list(order: Order):
    orders = order.orders
    print(orders)
    seq_list = [i['seq'] for i in orders]
    print(seq_list)
    return {
        "code" : 0,
        "message" : "数据处理成功！",
        "data" : seq_list
    }

@app.post("/v1/api/wms/produce_test")
async def produce_test():
    return {
        "code" : 0,
        "message" : "数据处理成功！",
        "data" : {"produce": 'started!' }
    }

# fake
@app.put("/v1/api/wms/warehouse/fake/{bin_id}")
async def update_warehouse_bin(bin_id: int, q: Optional[str] = None):
    isEmpty = 0
    # material_code = get_material_code(bin_id)
    # material_dict = get_material_dict
    # material_code = get_material_code(material_dict, bin_id)
    # print(material_code)
    materialList= generate_material_list_json(bin_id)
    query = warehouse.update().where(warehouse.c.id==bin_id).values(isEmpty=isEmpty, materialList=materialList)
    last_record_id = await database.execute(query)

    return_json = {
        "code" : 0,
        "message" : "数据处理成功！",
        "data" : {"id": last_record_id, "bin_id": bin_id}
    }
    return return_json


if __name__ == '__main__':
    uvicorn.run(app=app, host="0.0.0.0", port=8088, debug=True)        