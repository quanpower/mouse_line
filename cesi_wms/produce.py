import requests
import json


uri = 'http://172.16.1.62/aim-mes/open-api/order/produce/v1/list'

r = requests.get(uri)
return_json = r.json()
print(return_json)

'''{
	"code":0,
	"data":[
		{
			"customerCode":"SC0001",
			"customerName":"梁通",
			"id":5,
			"materialList":[
				{
					"materialCode":"Ba01.01",
					"materialName":"五号电池"
				},
				{
					"materialCode":"Ba02.06",
					"materialName":"粉色电池款电池盖"
				},
				{
					"materialCode":"La01.01",
					"materialName":"公制螺丝"
				},
				{
					"materialCode":"Na01.01",
					"materialName":"包装盒"
				},
				{
					"materialCode":"Za01.06",
					"materialName":"粉色电池款底壳"
				},
				{
					"materialCode":"Za02.06",
					"materialName":"粉色电池款中壳"
				},
				{
					"materialCode":"Za03.06",
					"materialName":"粉色电池款上壳"
				}
			],
			"productCode":"A02",
			"productName":"粉色电池款",
			"seq":"PP000005",
			"signType":0,
			"signValue":""
		},
		{
			"customerCode":"SC0002",
			"customerName":"李刚",
			"id":4,
			"materialList":[
				{
					"materialCode":"Ba01.01",
					"materialName":"五号电池"
				},
				{
					"materialCode":"Ba02.04",
					"materialName":"白色电池款电池盖"
				},
				{
					"materialCode":"La01.01",
					"materialName":"公制螺丝"
				},
				{
					"materialCode":"Na01.01",
					"materialName":"包装盒"
				},
				{
					"materialCode":"Za01.04",
					"materialName":"白色电池款底壳"
				},
				{
					"materialCode":"Za02.04",
					"materialName":"白色电池款中壳"
				},
				{
					"materialCode":"Za03.04",
					"materialName":"白色电池款上壳"
				}
			],
			"productCode":"A01",
			"productName":"白色电池款",
			"seq":"PP000004",
			"signType":0,
			"signValue":""
		},
		{
			"customerCode":"SC0001",
			"customerName":"梁通",
			"id":1,
			"materialList":[
				{
					"materialCode":"Ba01.01",
					"materialName":"五号电池"
				},
				{
					"materialCode":"Ba02.04",
					"materialName":"白色电池款电池盖"
				},
				{
					"materialCode":"La01.01",
					"materialName":"公制螺丝"
				},
				{
					"materialCode":"Na01.01",
					"materialName":"包装盒"
				},
				{
					"materialCode":"Za01.04",
					"materialName":"白色电池款底壳"
				},
				{
					"materialCode":"Za02.04",
					"materialName":"白色电池款中壳"
				},
				{
					"materialCode":"Za03.04",
					"materialName":"白色电池款上壳"
				}
			],
			"productCode":"A01",
			"productName":"白色电池款",
			"seq":"PP000001",
			"signType":2,
			"signValue":"http://172.16.1.62/pcs-file/sign/202101121914_1610450049906.jpg"
		},
		{
			"customerCode":"SC0001",
			"customerName":"梁通",
			"id":6,
			"materialList":[
				{
					"materialCode":"Ba01.01",
					"materialName":"五号电池"
				},
				{
					"materialCode":"Ba02.06",
					"materialName":"粉色电池款电池盖"
				},
				{
					"materialCode":"La01.01",
					"materialName":"公制螺丝"
				},
				{
					"materialCode":"Na01.01",
					"materialName":"包装盒"
				},
				{
					"materialCode":"Za01.06",
					"materialName":"粉色电池款底壳"
				},
				{
					"materialCode":"Za02.06",
					"materialName":"粉色电池款中壳"
				},
				{
					"materialCode":"Za03.06",
					"materialName":"粉色电池款上壳"
				}
			],
			"productCode":"A02",
			"productName":"粉色电池款",
			"seq":"PP000006",
			"signType":0,
			"signValue":""
		},
		{
			"customerCode":"SC0001",
			"customerName":"梁通",
			"id":3,
			"materialList":[
				{
					"materialCode":"Ba01.01",
					"materialName":"五号电池"
				},
				{
					"materialCode":"Ba02.05",
					"materialName":"黑色电池款电池盖"
				},
				{
					"materialCode":"La01.01",
					"materialName":"公制螺丝"
				},
				{
					"materialCode":"Na01.01",
					"materialName":"包装盒"
				},
				{
					"materialCode":"Za01.05",
					"materialName":"黑色电池款底壳"
				},
				{
					"materialCode":"Za02.05",
					"materialName":"黑色电池款中壳"
				},
				{
					"materialCode":"Za03.05",
					"materialName":"黑色电池款上壳"
				}
			],
			"productCode":"A03",
			"productName":"黑色电池款",
			"seq":"PP000003",
			"signType":0,
			"signValue":""
		},
		{
			"customerCode":"SC0001",
			"customerName":"梁通",
			"id":7,
			"materialList":[
				{
					"materialCode":"Ba01.01",
					"materialName":"五号电池"
				},
				{
					"materialCode":"Ba02.04",
					"materialName":"白色电池款电池盖"
				},
				{
					"materialCode":"La01.01",
					"materialName":"公制螺丝"
				},
				{
					"materialCode":"Na01.01",
					"materialName":"包装盒"
				},
				{
					"materialCode":"Za01.04",
					"materialName":"白色电池款底壳"
				},
				{
					"materialCode":"Za02.04",
					"materialName":"白色电池款中壳"
				},
				{
					"materialCode":"Za03.04",
					"materialName":"白色电池款上壳"
				}
			],
			"productCode":"A01",
			"productName":"白色电池款",
			"seq":"PP000007",
			"signType":0,
			"signValue":""
		},
		{
			"customerCode":"SC0002",
			"customerName":"李刚",
			"id":2,
			"materialList":[
				{
					"materialCode":"La01.01",
					"materialName":"公制螺丝"
				},
				{
					"materialCode":"Na01.01",
					"materialName":"包装盒"
				},
				{
					"materialCode":"Za01.03",
					"materialName":"粉色充电款底壳"
				},
				{
					"materialCode":"Za02.03",
					"materialName":"粉色充电款中壳"
				},
				{
					"materialCode":"Za03.03",
					"materialName":"粉色充电款上壳"
				}
			],
			"productCode":"B02",
			"productName":"粉色充电款",
			"seq":"PP000002",
			"signType":1,
			"signValue":"设计全方位，智能零距离。"
		}
	],
	"message":"操作成功!"
}'''


return_dict = json.loads(return_json)

print(return_dict)

return_data = return_dict['data']

print(return_data)

seq_list = []
for i in return_data:
    seq_list.append(i['seq'])


seq_list_str = ','.join(seq) for seq in seq_list

print(seq_list_str)

