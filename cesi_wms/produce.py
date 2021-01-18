import requests

uri = 'http://172.16.1.62/aim-mes/open-api/order/produce/v1/list'

r = requests.get(uri)
print(r.json())