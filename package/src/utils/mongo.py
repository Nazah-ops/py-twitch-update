import logging

from pymongo import MongoClient

client: MongoClient = None

def init_mongo_client():
    global client
    try:
        uri = "mongodb://root:rootpassword@raspdavid:27017/"
        client = MongoClient(uri)
        client.admin.command("ping")
        logging.info("MongoDB connected successfully")
    except Exception as e:
        raise Exception("Cannot connect to MongoDB: ", e)
    return

def get_mongo_client():
    global client
    if client == None:
        init_mongo_client()
    return client

def close_mongo_client():
    global client
    client.close();
    
def get_unused_id(query: dict, ids: list[str]):
    global client
    client = get_mongo_client()["db"]["scraper"]
    for id in ids:
        isUsedSound = client.count_documents({ "source" : query["source"], "idResult": id })
        if isUsedSound:
            continue
        client.insert_one({ **query, "idResult":id })
        return id
    
    """ All the sounds were used """
    client.delete_many(query)
    client.insert_one({ **query, "idResult": ids[0] })
    return ids[0]