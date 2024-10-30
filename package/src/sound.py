import logging
import os
from uuid import uuid4
import json
from utils.download import download
from requests import get
from utils.globals import work_dir
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
        return json.loads(response.text)
        
        
    def download_sound(self, query, tag):
        logging.info(f"Handling download of audio effect, query:{query}, tag:{tag}")
        query_list = self.get_sound_list(query, tag)
        url = f'https://freesound.org/apiv2/sounds/{query_list["results"][0]["id"]}/'
        params = {
            "token": os.environ.get("FREESOUND_API_KEY"),
        }
        response = get(url, params=params)
        url = json.loads(response.text)["previews"]["preview-hq-mp3"]
        
        audio_name = work_dir(f"{uuid4()}.mp3")
        logging.info(f"Downloaded audio effect: {audio_name}")
        download(url, audio_name)
        return audio_name