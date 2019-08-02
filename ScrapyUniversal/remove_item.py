import pymongo

client = pymongo.MongoClient("mongodb://admin:admin@192.168.11.30:27017/admin")
bus_xy = client['bus_xy']['bus_xy']
station_xy = client['bus1']['station_xy']
m = 0
# for i in (bus_xy.find(projection={'_id': False, 'bus_num': 1, 'bus_list': 1})):
#     if m > 158:
#         bus_xy.delete_one(i)
#     m += 1

for i in (station_xy.find()):
    print(i)
    station_xy.delete_one(i)
