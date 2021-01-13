from typing import Optional
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

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

order_sample={
    "code":0,
    "message":"string",
    "data":[
        {
            "seq":"PP000001",
            "customerCode":"SC0001",
            "customerName":"张三",
            "productCode":"A01",
            "productName":"白色电池款",
            "signType":2,
            "signValue":"http:xxx.jpeg",
            "materialList":[
                {
                    "materialCode":"Za01.01",
                    "materialName":"白色底壳"
                },
                {
                    "materialCode":"Za02.01",
                    "materialName":"中壳"
                },
                {
                    "materialCode":"Za03.01",
                    "materialName":"白色上壳"
                },
                {
                    "materialCode":"Ba01.01",
                    "materialName":"电池"
                },
                {
                    "materialCode":"Ba02.01",
                    "materialName":"电池盖"
                },
                {
                    "materialCode":"La01.01",
                    "materialName":"公制螺丝"
                }
            ]
        },
        {
            "seq":"PP000002",
            "customerCode":"SC0002",
            "customerName":"李四",
            "productCode":"B01",
            "productName":"白色充电款",
            "signType":1,
            "signValue":"开心",
            "materialList":[
                {
                    "materialCode":"Za01.01",
                    "materialName":"白色底壳"
                },
                {
                    "materialCode":"Za02.01",
                    "materialName":"中壳"
                },
                {
                    "materialCode":"Za03.01",
                    "materialName":"白色上壳"
                },
                {
                    "materialCode":"La01.01",
                    "materialName":"公制螺丝"
                }
            ]
        }
    ]
}


@app.put("/v1/api/order/produce/list")
def update_order_list(order: Order):
    orders = order.orders
    print(orders)
    seq_list = [i['seq'] for i in orders]
    print(seq_list)
    return {
        "code" : 0,
        "message" : "数据处理成功！",
        "data" : seq_list
    }

@app.get("/v1/api/wms/warehouse/snapshot/list")
def get_warehouse_snapshot(ver: Optional[int] = None):
    return_json = {
        "code" : 0,
        "message" : "数据处理成功！",
        "data" : [
            {
            "ver":1,
            "snapshot":[
                {
                    "locatorCode":"011",
                    "materialList":[
                        {
                            "materialCode":"Ba01.01",
                            "materialPlace":"8"
                        },
                        {
                            "materialCode":"Ba01.02",
                            "materialPlace":"9"
                        }
                    ]
                },
                {
                    "locatorCode":"012",
                    "materialList":[
                        {
                            "materialCode":"Ba01.01",
                            "materialPlace":"7"
                        },
                        {
                            "materialCode":"Ba01.02",
                            "materialPlace":"9"
                        }
                    ]
                },
                {
                    "locatorCode":"021",
                    "materialList":[
                        {
                            "materialCode":"Ba02.01",
                            "materialPlace":"1"
                        },
                        {
                            "materialCode":"Ba02.02",
                            "materialPlace":"5"
                        },
                        {
                            "materialCode":"Ba02.03",
                            "materialPlace":"7"
                        }
                    ]
                }
            ],
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
        }]
    }
    return return_json

@app.get("/v1/api/wms/warehouse/bin/{bin_id}")
def get_warehouse_bin(bin_id: int, q: Optional[str] = None):
    return_json = {
        "code" : 0,
        "message" : "数据处理成功！",
        "data" : [
            {"bin_name": bin_id, "bin_id": bin_id}
        ]  
    }
    return return_json

@app.get("/v1/api/wms/line_storage/snapshot/list")
def get_line_storage_snapshot(ver: Optional[int] = None):
    return_json = {
        "code" : 0,
        "message" : "数据处理成功！",
        "data" : [
            {
                "ver":1,
                "snapshot":[
                    {
                        "lineStorageCode":" LineStorage1",
                        "materialList":[
                            {
                                "materialCode":"Ba01.01",
                                "materialPlace":"8"
                            },
                            {
                                "materialCode":"Ba01.02",
                                "materialPlace":"9"
                            }
                        ]
                    },
                    {
                        "lineStorageCode":" LineStorage2",
                        "materialList":[
                            {
                                "materialCode":"Ba01.01",
                                "materialPlace":"7"
                            },
                            {
                                "materialCode":"Ba01.02",
                                "materialPlace":"9"
                            }
                        ]
                    },
                    {
                        "lineStorageCode":" LineStorage3",
                        "materialList":[
                            {
                                "materialCode":"Ba02.01",
                                "materialPlace":"1"
                            },
                            {
                                "materialCode":"Ba02.02",
                                "materialPlace":"5"
                            },
                            {
                                "materialCode":"Ba02.03",
                                "materialPlace":"7"
                            }
                        ]
                    }
                ],
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
            }
        ]  
    }
    return return_json


if __name__ == '__main__':
    uvicorn.run(app=app,host="0.0.0.0",port=8088,debug=True)    