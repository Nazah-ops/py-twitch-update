import datetime
import json
import os
from os.path import join

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv


class Twitch:
    
    def __init__(self):
        dotenv_path = join(os.path.abspath(os.curdir), '.env')
        load_dotenv(dotenv_path)
        
        #Sending request to Twitch to get token credential
        payload = {
            'client_id' : os.environ.get('CLIENT_ID'),
            'client_secret': os.environ.get("CLIENT_SECRET"),
            'grant_type': 'client_credentials'
        }
        response = requests.post("https://id.twitch.tv/oauth2/token", headers={'Content-Type': 'application/x-www-form-urlencoded'}, data=payload)
        token = json.loads(response.text)["access_token"]
        self.headers = {'Authorization': f'Bearer {token}', 'Client-Id': os.environ.get("CLIENT_ID")}

    @staticmethod
    def get_streamers():
        '''
        Retreive from a third party website the list of the most watched streamers, the first 100
        Returns a list of strings
        '''
        results = []
        request = requests.get('https://www.twitchmetrics.net/channels/viewership?game=League+of+Legends&lang=en&page=1')
        parsed_html = BeautifulSoup(request.text, features="html.parser")

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

    def download_clip(self,clip):
        file = f'{clip["title"]}.mp4'.replace("/","slash").replace(" ","")
        path = "/app/files/clips/" + file;


        index = clip["thumbnail_url"].find('-preview')
        clip_url = clip["thumbnail_url"][:index] + '.mp4'
        r = requests.get(clip_url)

        if r.headers['Content-Type'] != 'binary/octet-stream':
            raise Exception(f'Failed to download clip from thumb: {clip["thumbnail_url"]}')


        if not os.path.exists('files/clips'): os.makedirs('files/clips')

        with open(path, 'wb') as f:
            f.write(r.content)

        #Get video length
        import cv2
        video = cv2.VideoCapture(path)

        duration = video.get(cv2.CAP_PROP_POS_MSEC)

        #Slice video from last 3 seconds
        sliced = "sliced" + file
        slicedPath = "/app/files/clips/" + sliced

        from moviepy.editor import VideoFileClip

        # Load the video clip
        video_clip = VideoFileClip(path)

        # Slice the video clip
        sliced_clip = video_clip.subclip(duration, duration - ((duration/100) * 20))

        # Write the sliced clip to a new file
        sliced_clip.write_videofile(slicedPath, codec="libx264", audio_codec="aac")

        return sliced
        