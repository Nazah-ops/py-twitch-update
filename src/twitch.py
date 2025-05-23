import requests
import os
import json
import datetime

from os.path import join
from dotenv import load_dotenv
from bs4 import BeautifulSoup

class Twitch:
    
    def __init__(self):
        dotenv_path = join(os.path.abspath(os.curdir), '.env')
        load_dotenv(dotenv_path)
        
        #Sending request to Twitch to get token credential
        payload = {
            'client_id' : os.environ.get("CLIENT_ID"),
            'client_secret': os.environ.get("CLIENT_SECRET"),
            'grant_type': 'client_credentials'
        }
        response = requests.post("https://id.twitch.tv/oauth2/token", headers={'Content-Type': 'application/x-www-form-urlencoded'}, data=payload)
        token = json.loads(response.text)["access_token"]
        self.headers = {'Authorization': f'Bearer {token}', 'Client-Id': os.environ.get("CLIENT_ID")}

    @staticmethod
    def get_streamers():
        '''
        Retreive from a third party website the list of the most watched streamers
        Returns a list of strings
        '''
        results = []
        request = requests.get('https://www.twitchmetrics.net/channels/viewership?game=League+of+Legends&lang=en&page=1')
        parsed_html = BeautifulSoup(request.text)

        for name in parsed_html.body.find_all('h5', attrs={'class':'mr-2 mb-0'}):
            results.append(name.get_text())
        
        return results


    def convert_name_to_id(self, name):
        '''
            Converts the basic name (e.g. Thebausffs) to the broadcaster id, which twitch uses to identify the streamer
            There are some exceptions with names, that involve whitespaces between them: only staff members can use them, and when putting
            the name in the endpoint will result in a error, so the name has to be stripped of it
        '''
        if str.isspace(name):
            return None
        
        params = { "login" : "".join(name.split()) }
        request = requests.get(f'https://api.twitch.tv/helix/users', headers=self.headers, params=params)
        if request.ok:
            return json.loads(request.text)["data"][0]["id"]
        else:
            raise Exception(f'Error from twitch endpoint {request.text}')

    def clips_from_broadcaster_id(self, id):
        '''Retreives the clips from a streamer, based also on timeframe, and sorted by views'''
        format_time = "%Y-%m-%dT%H:%M:%SZ"
        params = {
            "broadcaster_id" : id,
            "started_at" : (datetime.datetime.now() - datetime.timedelta(days=3)).strftime(format_time),
            "ended_at" : datetime.datetime.now().strftime(format_time)
        }
        request = requests.get(f'https://api.twitch.tv/helix/clips', headers=self.headers, params=params)
        return json.loads(request.text)["data"]

    def download_clip(clip):
        path = f'files/clips/{clip["title"]}.mp4'
        index = clip["thumbnail_url"].find('-preview')
        clip_url = clip["thumbnail_url"][:index] + '.mp4'
        r = requests.get(clip_url)

        if r.headers['Content-Type'] == 'binary/octet-stream':
            if not os.path.exists('files/clips'): os.makedirs('files/clips')
            with open(path, 'wb') as f:
                f.write(r.content)
            return path
        else:
            raise Exception(f'Failed to download clip from thumb: {clip["thumbnail_url"]}')
        