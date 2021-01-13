from typing import Optional
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


@app.put("/v1/api/order/produce/list")
def update_order_list():
    return {
        "code" : 0,
        "message" : "数据处理成功！",
        "data" : []
    }

@app.get("/v1/api/wms/warehouse/snapshot/list")
def get_warehouse_snapshot(q: Optional[str] = None):
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
def get_line_storage_snapshot(q: Optional[str] = None):
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