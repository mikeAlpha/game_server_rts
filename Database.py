import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

user_db = myclient["All_Users"]

user_col = user_db["User_data"]

query = {}

def Update():
    document = user_col.find_one(query)

def UpdateQuery(q):
    global query
    query = q
