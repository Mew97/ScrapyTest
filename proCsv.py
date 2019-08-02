import json

with open('bus0.json', "r", encoding="utf-8") as load_f:
    load_dict = json.load(load_f)
    load_f.close()

stations = {}
relationship = []
id0 = 0
for buses in load_dict:
    if load_dict[buses]:
        for station in load_dict[buses]:
            info = load_dict[buses][station]
            if station not in stations:
                id0 += 1
                stations.setdefault(station,
                                    {"id": id0, "x": info[0], "y": info[1], "label": [buses.replace("公交车路线", ""), ]})
            else:
                stations[station]["label"].append(buses.replace("公交车路线", ""))
        list_bus = list(load_dict[buses])
        for i in range(0, len(list_bus) - 1):
            buses = buses.replace("公交车路线", "")
            relationship.append((stations[list_bus[i]]["id"], stations[list_bus[i + 1]]["id"], buses))
            relationship.append((stations[list_bus[i + 1]]["id"], stations[list_bus[i]]["id"], buses))

# print(stations)


with open("node.csv", "w", encoding="utf-8") as node_f:
    node_f.writelines("id:ID(Station),name:String,x:String,y:String,:Label\n")
    for station in stations:
        label = "station"
        node_f.writelines(str(stations[station]["id"]) + "," + station + "," + str(stations[station]["x"]) + "," + str(
            stations[station]["y"]) + "," + label + "\n")
    node_f.close()

with open("relationship.csv", "w", encoding="utf8") as relationship_f:
    relationship_f.writelines(":START_ID(Station),:END_ID(Station),:TYPE\n")
    for i in relationship:
        relationship_f.writelines(str(i[0]) + "," + str(i[1]) + "\n")
        # relationship_f.writelines(str(i[0])+","+str(i[1])+"," + i[2] + "\n")
