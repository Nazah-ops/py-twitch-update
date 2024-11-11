import json
import logging
import os
from uuid import uuid4

from requests import get

from utils.download import download
from utils.globals import work_dir
from utils.mongo import get_unused_id


class Sound:
    def __init__(self):
        pass
    
    def get_sound_list(self, query, tag):
        url = "https://freesound.org/apiv2/search/text/"
        params = {
            "query": query,
            "token": os.environ.get("FREESOUND_API_KEY"),
            "filter": f"tag:{tag}",
            "sort": "rating_desc"
        }
        
        response = get(url, params=params)
        return json.loads(response.text)["results"]
        
    def download_sound(self, query, tag):
        logging.info(f"Handling download of audio effect, query:{query}, tag:{tag}")
        id = get_unused_id({"source" : "freesound.org", "query": query, "tag": tag}, self.get_sound_list(query, tag), 'id')["id"]
        url = f'https://freesound.org/apiv2/sounds/{id}/'
        params = {
            "token": os.environ.get("FREESOUND_API_KEY"),
        }
        response = get(url, params=params)
        url = json.loads(response.text)["previews"]["preview-hq-mp3"]
        
        audio_name = work_dir(f"{uuid4()}.mp3")
        logging.info(f"Downloaded audio effect: {audio_name}")
        download(url, audio_name)
        return audio_name