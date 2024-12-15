from dataclasses import is_dataclass
import logging as logger
from datetime import datetime
import os
from typing import Any, List

from pymongo import MongoClient

client: MongoClient = None

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
    if client == None:
        init_mongo_client()
    return client

def close_mongo_client():
    global client
    client.close();
    
    
    
def trova_per_valori(obj_list: List[Any], field_name: List[str], values: List[Any]) -> List[Any]:
    """
    Filtra una lista di istanze di dataclass in cui il valore del campo specificato corrisponde a uno dei valori nella lista fornita.

    :param obj_list: Lista di istanze di dataclass.
    :param field_name: Percorso del campo come lista di stringhe per supportare campi non stringa.
    :param values: Lista di valori da cercare nel campo specificato.
    :return: Lista di oggetti che corrispondono al criterio.
    """
    def get_nested_value(obj, field_path):
        """
        Ritorna il valore di un campo annidato.
        """
        for field in field_path:
            if is_dataclass(obj):
                obj = getattr(obj, field, None)
            else:
                return None
        return obj

    # Restituisce solo gli oggetti il cui valore nel campo specificato non è presente nella lista "values"
    return [obj for obj in obj_list if get_nested_value(obj, field_name) not in values]

def get_unused_id_dict(query: dict, objects: list[Any], id_key: List[str]):
    """
        Esegue una chiamata al backend, per controllare se quali id trovati con la query fornita sia gia' stato utilizzato, restituendo un id inutilizzato.
        Se tutti gli id forniti dovessero essere gia' stati utilizzati, allora pulisce tutti gli id a backend, per poi continuare il ciclo.
        Questa funzione permette di utilizzare tutti gli id costantemente senza sovrapporli
        Parametri: query: con cui si trovano gli id, objects: gli id trovati, 
    """
    client = get_mongo_client()["db"]["scraper"]
    now = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    for object in objects:
        used_keys = client.find({query** })
        object_id = trova_per_valori(object, used_keys, id_key)
        client.insert_one({ **query, "idResult":object_id, "createdAt": now })
        return object
    
    """ All the elements were used """
    logger.info("All the sources were used, resetting..")
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
