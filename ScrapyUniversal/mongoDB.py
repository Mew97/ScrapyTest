import pymongo
import requests
from urllib.parse import urlencode
import re


def get_xy(place):
    params = {
        "address": place,
        "output": "json",
        "ak": "twmEUDaj5N5h1vUGPIqrvL9oeTsPKcsv",
        "callback": "showLocation",
        "city": "武汉市"
    }
    url = 'http://api.map.baidu.com/geocoding/v3/?' + urlencode(params)

    response = requests.get(url)
    if response.status_code == 200:
        rs = re.findall('([0-9]+[.][0-9]*)', response.text)
        print(rs)
        if not rs:
            raise RuntimeError("未找到坐标")
        else:
            return rs


client = pymongo.MongoClient("mongodb://admin:admin@192.168.11.30:27017/admin")
db = client['bus1']
bus = db.get_collection(db.list_collection_names()[0])
bus_xy = client['bus_xy']['bus_xy']
m, n = 0, 0
for i in (bus.find(projection={'_id': False, 'bus_num': 1, 'bus_list': 1})):
    place_xy = {}
    m += 1
    if m <= 158:
        continue

    for j in i["bus_list"]:
        n += 1
        print(n, j)
        place_xy.setdefault(j.replace(".", "。"), get_xy(j))
    i["bus_list"] = place_xy
    print(m, i)
    bus_xy.insert(i)

# s = set()
# for i in list(bus.find(projection={'_id': False})):
#     s = s.union(set(i["bus_list"]))
# print(len(s))



# print(get_xy())
