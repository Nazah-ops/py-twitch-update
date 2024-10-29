import http.client
import urllib.parse
import os
import uuid
import json
from utils.download import download
class Sound:
    def __init__(self):
        pass
    
    def get_sound_list(self, query, tag):
        conn = http.client.HTTPSConnection("freesound.org")
        
        params = {
            "query": query,
            "token": os.environ.get("FREESOUND_API_KEY"),
            "filter": f"tag:{tag}",
            "sort": "rating_desc"
        }
        endpoint = f"/apiv2/search/text/?{urllib.parse.urlencode(params)}"
        conn.request("GET", endpoint)
        
        res = conn.getresponse()
        return json.loads(res.read().decode("utf-8"))
        
        
    def download_sound(self, query, tag):
        query_list = self.get_sound_list(query, tag)
        conn = http.client.HTTPSConnection("freesound.org")
        params = {
            "token": os.environ.get("FREESOUND_API_KEY"),
        }
        conn.request("GET", f'/apiv2/sounds/{query_list["results"][0]["id"]}/?{urllib.parse.urlencode(params)}')
        res = conn.getresponse()
        url = json.loads(res.read().decode("utf-8"))["previews"]["preview-hq-mp3"]
        audio_name = f"/app/files/{uuid.uuid4().hex[:6].upper()}.mp3"
        download(url, audio_name)
        return audio_name