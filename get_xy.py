import pymongo
import requests
from urllib.parse import urlencode
import re
import json


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
        return rs
    else:
        return []
        # if not rs:
        #     raise RuntimeError("未找到坐标")
        # else:
        #     return rs


client = pymongo.MongoClient("mongodb://admin:admin@192.168.11.30:27017/admin")
db = client['bus1']
# bus = db.get_collection(db.list_collection_names()[0])
# s = set()
# for i in (bus.find(projection={'_id': False, 'bus_num': 1, 'bus_list': 1})):
#     s = s.union(set(i["bus_list"]))
#
station = db['station']
station_xy = db['station_xy']
station_xy1 = db['station_xy1']
# m = 0
# for i in station.find(projection={'_id': False, 'station': 1}):
#     m += 1
#     if m <= 2279:
#         continue
#
#     i = dict(i)
#     i.setdefault('coordinate', get_xy(i["station"]))
#
#     print(m, i)
#     station_xy.insert(i)

# count = 0
# for i in station_xy.find(projection={'_id': False, 'station': 1,'coordinate': 1}):
#     if i['coordinate']:
#         l = [float(i['coordinate'][0]), float(i['coordinate'][1])]
#         i['coordinate'] = l
#         station_xy1.insert(i)
#         count += 1
# print(count)

# for i in db['bus'].find(projection={'_id': False, 'bus_num': 1, 'bus_list': 1}):
#     try:
#         i['bus_list'].index('东沟路采摘园')
#         print(i)
#     except:
#         continue

d = {}
for i in station_xy1.find(projection={'_id': False, 'station': 1,'coordinate': 1}):
    d.setdefault(i['station'], i['coordinate'])

print(len(d))

# with open("bus.json", "w", encoding="utf-8") as f:
#     for i in db['bus'].find(projection={'_id': False, 'bus_num': 1, 'bus_list': 1}):
#         for j in i['bus_list']:
#             f.writelines(i['bus_num'] + " " + j + " " + str(d[j][0]) + " " + str(d[j][1]) + "\n")
#     f.close()
new_d = {}
for i in db['bus'].find(projection={'_id': False, 'bus_num': 1, 'bus_list': 1}):
    # new_d.setdefault(i['bus_num'], {})
    count = 0
    b_list = []
    for j in i['bus_list']:
        count += 1
        b_list.append({'num':count,'station':j,'coordinate':d[j]})
    # new_d[i['bus_num']].setdefault(j, {count: tuple(d[j])})
    new_d.setdefault(i['bus_num'], b_list)


with open("bus.json", "w", encoding="utf-8") as f:
    json.dump(new_d, f, ensure_ascii=False, indent=4)
    f.close()


