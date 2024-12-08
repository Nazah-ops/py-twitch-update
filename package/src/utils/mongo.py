import logging
from datetime import datetime

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
    

def get_unused_id_dict(query: dict, objects: list[dict], id_key: str):
    """
        Esegue una chiamata al backend, per controllare se quali id trovati con la query fornita sia gia' stato utilizzato, restituendo un id inutilizzato.
        Se tutti gli id forniti dovessero essere gia' stati utilizzati, allora pulisce tutti gli id a backend, per poi continuare il ciclo.
        Questa funzione permette di utilizzare tutti gli id costantemente senza sovrapporli
        Parametri: query: con cui si trovano gli id, objects: gli id trovati, 
    """
    client = get_mongo_client()["db"]["scraper"]
    now = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    for object in objects:
        object_id = find_key_in_dict(object, id_key)
        is_used = client.count_documents({ "source" : query["source"], "idResult": object_id })
        if is_used:
            continue
        client.insert_one({ **query, "idResult":object_id, "createdAt": now })
        return object
    
    """ All the elements were used """
    logging.info("All the sources were used, resetting..")
    object_id = find_key_in_dict(objects[0], id_key)
    client.delete_many(query)
    client.insert_one({ **query, "idResult": object_id, "createdAt": now })
    return objects[0]

def find_key_in_dict(json, nome_chiave):
    # Se la chiave è presente al livello corrente, restituisci il valore
    if nome_chiave in json:
        return json[nome_chiave]
    # Altrimenti, cerca nelle sottostrutture se sono dizionari
    for chiave, valore in json.items():
        if isinstance(valore, dict):
            risultato = find_key_in_dict(valore, nome_chiave)
            if risultato is not None:
                return risultato
    return None
