import pymongo
import json
import datetime

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

user_db = myclient["All_Users"]

user_col = user_db["User_data"]

building_db = myclient["building_data"]

building_col = building_db["all_data"]

clients_to_be_updated = {}

def syncplayerdata(user_id):
    print(user_id)
    val = user_col.find_one({"_user_id" : user_id})
    return json.dumps(val["_all_data"]["PlayerSaveData"])
    
async def add_building(user_id,buildingType,x,y,z,c):
    print("adding building")
    user_query = {"_user_id": user_id}
    val = user_col.find_one(user_query)
    city_data = val["_all_data"]["PlayerSaveData"]["allCityData"]

    count = user_col.aggregate([
    {"$match": user_query},
    {"$project": {"count": {"$size": "$_all_data.PlayerSaveData.allCityData"}}}
    ])

    totalBuildingCount = next(count)['count']
    
    get_building_type = building_col.find_one({"buildingType":buildingType})
    totaltimefromdb = get_building_type["EstablishingTime"]
    endTime = datetime.datetime.utcnow() + datetime.timedelta(seconds=totaltimefromdb)

    new_building = { "worldPos": {
                                    "x": x,
                                    "y": y,
                                    "z": z
                                        },
                              "localScale": {
                                    "x": 1,
                                    "y": 1,
                                    "z": 1
                                        },
                              "maxScale": {
                                    "x": 1,
                                    "y": 1,
                                    "z": 1
                                        },
                              "buildingLevel": 0,
                              "upgradeEndTime": endTime,
                              "upgradeBuildTime": totaltimefromdb,
                              "isUpgrading": False,
                              "isEstablishing": True
                    }
    i = 0
    totaltimefromdb = 0
    for x in city_data:
        if x["buildingType"] == buildingType:
            user_col.update_one(user_query,{"$push": {f"_all_data.PlayerSaveData.allCityData.{i}.createdBuildings": new_building}})
            count = user_col.aggregate([{"$match": user_query},{"$project": {"count": {"$size": f"$_all_data.PlayerSaveData.allCityData{i}.createdBuildings"}}}])
            id = 6
            val = str(id) + '_' + str(buildingType)+ '&' + str(count-1)+ '&' + str(totaltimefromdb) + '&' + str(endTime)
            dat = bytes(val,'utf-8')
            buffer = bytearray()
            buffer.extend(dat)
            print(len(dat))
            c.send(dat)
            break
        elif i == totalBuildingCount:
            print("Creating a new building type")
            new_building_data = {
                    "buildingType": buildingType,
                    "maxStructureCount": 0,
                    "createdBuildings": [new_building],
                    "buildingGenerationData": {
                    "currentStructureCount": 0,
                    "isUnLocked": False,
                    "unlockAtMainBuildingLevel": 0,
                    "requiredCurrenciesToEstablish": [],
                    "buildingGenerationInfoList": []
                    }
            }
            user_col.update_one(user_query,{"$push": {"_all_data.PlayerSaveData.allCityData": new_building_data}})
            id = 6
            val = str(id) + '_' + str(buildingType)+ '&' + str(0)+ '&' + str(totaltimefromdb) + '&' + str(endTime)
            dat = bytes(val,'utf-8')
            buffer = bytearray()
            buffer.extend(dat)
            print(len(dat))
            c.send(dat)
            break
        i += 1

async def add_building_complete(user_id,buildingType,childIndex,c):
    print("adding building")
    user_query = {"_user_id": user_id}
    val = user_col.find_one(user_query)
    city_data = val["_all_data"]["PlayerSaveData"]["allCityData"]
    i = 0
    for x in city_data:
        if x["buildingType"] == buildingType:
            query = {"_user_id": user_id}
            update_building_dat_1 = {"$set": {f"_all_data.PlayerSaveData.allCityData.{i}.createdBuildings.{childIndex}.isEstablishing": False}}
            user_col.update_one(query, update_building_dat_1)

            update_building_dat_2 = {"$set": {f"_all_data.PlayerSaveData.allCityData.{i}.createdBuildings.{childIndex}.upgradeEndTime": "0"}}
            user_col.update_one(query, update_building_dat_2)

            update_building_dat_3 = {"$set": {f"_all_data.PlayerSaveData.allCityData.{i}.createdBuildings.{childIndex}.upgradeBuildTime": 0}}
            user_col.update_one(query, update_building_dat_3)
                
            id = 7
            val = str(id) + '_' + str(buildingType)+ '&' + str(childIndex)
            dat = bytes(val,'utf-8')
            buffer = bytearray()
            buffer.extend(dat)
            print(len(dat))
            c.send(dat)
            break
        i += 1

async def update_build_position(user_id,buildingType,childIndex,x,y,z,c):
    print(f"updating building position for {user_id} , {buildingType} , {childIndex} , {x} , {y} , {z}")
    val = user_col.find_one({"_user_id" : user_id})
    city_data = val["_all_data"]["PlayerSaveData"]["allCityData"]
    i = 0
    for k in city_data:
        if k["buildingType"] == buildingType:
            query = {"_user_id": user_id}
            
            update_ugrade_dat_x = {"$set": {f"_all_data.PlayerSaveData.allCityData.{i}.createdBuildings.{childIndex}.worldPos.x": x}}
            update_ugrade_dat_y = {"$set": {f"_all_data.PlayerSaveData.allCityData.{i}.createdBuildings.{childIndex}.worldPos.y": y}}
            update_ugrade_dat_z = {"$set": {f"_all_data.PlayerSaveData.allCityData.{i}.createdBuildings.{childIndex}.worldPos.z": z}}
            
            user_col.update_one(query, update_ugrade_dat_x)
            user_col.update_one(query, update_ugrade_dat_y)
            user_col.update_one(query, update_ugrade_dat_z)

            id = 5

            dat  = bytes(str(id) + '_' +'Position Updated','utf-8')
            buffer = bytearray()
            buffer.extend(dat)

            c.send(buffer)
            break
        i += 1

async def upgrade_building(user_id,buildingType,childIndex,c):
    val = user_col.find_one({"_user_id" : user_id})
    city_data = val["_all_data"]["PlayerSaveData"]["allCityData"]
    get_current_building_level = 0
    i = 0
    totaltimefromdb = 0
    for x in city_data:
        if x["buildingType"] == buildingType:
            query = {"_user_id": user_id}
            update_ugrade_dat_1 = {"$set": {f"_all_data.PlayerSaveData.allCityData.{i}.createdBuildings.{childIndex}.isUpgrading": True}}
            user_col.update_one(query, update_ugrade_dat_1)
                
            get_building_type = building_col.find_one({"buildingType":buildingType})
            get_current_building_level = val["_all_data"]["PlayerSaveData"]["allCityData"][i]["createdBuildings"][childIndex]["buildingLevel"]
            totaltimefromdb = get_building_type["Levels"]["Level_" + str(get_current_building_level + 1)]
            
            # convert the end time to hours, minutes and seconds over here and then send the values to datetime.timedelta 
            
            endTime = datetime.datetime.utcnow() + datetime.timedelta(seconds=totaltimefromdb)
            
            
            print('totalTime: ' + str(totaltimefromdb))

            update_end_time = {"$set": {f"_all_data.PlayerSaveData.allCityData.{i}.createdBuildings.{childIndex}.upgradeEndTime":str(endTime)}}
            user_col.update_one(query, update_end_time)

            update_build_time = {"$set": {f"_all_data.PlayerSaveData.allCityData.{i}.createdBuildings.{childIndex}.upgradeBuildTime": totaltimefromdb}}
            user_col.update_one(query, update_build_time)
            
            id = 3

            val = str(id) + '_' + str(buildingType)+ '&' + str(childIndex)+ '&' + str(totaltimefromdb) + '&' + str(endTime)
            dat  = bytes(val,'utf-8')
            buffer = bytearray()
            buffer.extend(dat)
            print(len(dat))
            c.send(buffer)
            break
        i += 1

async def update_building_details(user_id,buildingType,childIndex,c):
    val = user_col.find_one({"_user_id" : user_id})
    city_data = val["_all_data"]["PlayerSaveData"]["allCityData"]
    get_current_building_level = 0
    i = 0
    for x in city_data:
        if x["buildingType"] == buildingType:
            query = {"_user_id": user_id}
            update_ugrade_dat_1 = {"$set": {f"_all_data.PlayerSaveData.allCityData.{i}.createdBuildings.{childIndex}.isUpgrading": False}}
            user_col.update_one(query, update_ugrade_dat_1)

            update_ugrade_dat_2 = {"$set": {f"_all_data.PlayerSaveData.allCityData.{i}.createdBuildings.{childIndex}.upgradeEndTime": "0"}}
            user_col.update_one(query, update_ugrade_dat_2)

            update_ugrade_dat_3 = {"$set": {f"_all_data.PlayerSaveData.allCityData.{i}.createdBuildings.{childIndex}.upgradeBuildTime": 0}}
            user_col.update_one(query, update_ugrade_dat_3)

            get_current_building_level = val["_all_data"]["PlayerSaveData"]["allCityData"][i]["createdBuildings"][childIndex]["buildingLevel"]

            update_building_level = get_current_building_level + 1

            update_ugrade_dat_4 = {"$set": {f"_all_data.PlayerSaveData.allCityData.{i}.createdBuildings.{childIndex}.buildingLevel": update_building_level}}
            user_col.update_one(query, update_ugrade_dat_4)
                
            id = 4
            val = str(id) + '_' + str(buildingType)+ '&' + str(childIndex)+'&' + str(update_building_level)
            dat = bytes(val,'utf-8')
            buffer = bytearray()
            buffer.extend(dat)
            print(len(dat))
            c.send(dat)

            break
        i += 1


