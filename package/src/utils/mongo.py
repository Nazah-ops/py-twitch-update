import logging as logger
import os
from datetime import datetime
from typing import Any, List, Optional, Union

from pymongo import MongoClient

client: Optional[MongoClient] = None

def init_mongo_client():
    global client
    try:
        user : str = os.environ.get('MONGODB_USER') or "default_mongo_user"
        password : str = os.environ.get('MONGODB_PASSWORD') or "default_mongo_password"
        address : str = os.environ.get('MONGODB_ADDRESS') or "default_mongo_address"
        uri = f"mongodb://{user}:{password}@{address}/"
        client = MongoClient(uri)
        client.admin.command("ping")
        logger.info("MongoDB connected successfully")
    except Exception as e:
        raise Exception("Cannot connect to MongoDB: ", e)
    return

def get_mongo_client():
    global client
    if client is not None:
        return client
    init_mongo_client()
    return client

def close_mongo_client():
    global client
    if client is not None:
        client.close();
    
    
    
def get_unused_id_dict(query: dict, data_objects: list[Any], id_path: List[str]):
    """
        Esegue una chiamata al backend, per controllare se quali id trovati con la query fornita sia gia' stato utilizzato, restituendo un id inutilizzato.
        Se tutti gli id forniti dovessero essere gia' stati utilizzati, allora pulisce tutti gli id a backend, per poi continuare il ciclo.
        Questa funzione permette di utilizzare tutti gli id costantemente senza sovrapporli
        Parametri: query: con cui si trovano gli id, objects: gli id trovati, 
    """
    if get_field_by_path(data_objects[0], id_path) is None:
        raise Exception("Given dataclass has no id, stopping execution")
    
    db = get_mongo_client()
    assert db is not None, "Db non inizializzato"

    collection = db["db"]["scraper"]
    saved_ids: set[str] = set([doc["idResult"] for doc in collection.find({**query}, {"idResult": 1, "_id": 0})])
    now = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    first = find_first_missing(data_objects=data_objects, id_path=id_path, saved_ids=saved_ids)
    
    if first:
        collection.insert_one({ **query, "idResult": get_field_by_path(first, id_path), "createdAt": now })
        return first
    
    """ All the elements were used """
    logger.info("All the sources were used, resetting..")
    collection.delete_many({**query})
    collection.insert_one({ **query, "idResult": get_field_by_path(data_objects[0], id_path), "createdAt": now })
    return data_objects[0]



def find_first_missing(data_objects: List[Any], id_path: List[str], saved_ids: set[str]) -> Any:
    """
    Trova il primo oggetto il cui ID (specificato dal percorso) non è presente nei saved_ids.
    """
    for obj in data_objects:
        object_id = get_field_by_path(obj, id_path)
        if object_id and object_id not in saved_ids:
            return obj  # Ritorna il primo oggetto mancante
    return None  # Nessun oggetto mancante trovato

from typing import Any, List


def get_field_by_path(obj: Any, path: List[str]) -> Any:
    """
    Accede a un campo di un dataclass annidato seguendo un percorso specificato come lista di attributi.
    """
    for attr in path:
        if not hasattr(obj, attr):
            return None  # Il percorso non è valido
        obj = getattr(obj, attr)
    return obj

