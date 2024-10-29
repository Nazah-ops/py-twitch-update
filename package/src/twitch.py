import datetime
import json
import os
from os.path import dirname, join

import requests
from bs4 import BeautifulSoup


class Twitch:
    
    def __init__(self):
        payload = {
            'client_id' : os.environ.get('TWITCH_CLIENT_ID'),
            'client_secret': os.environ.get("TWITCH_CLIENT_SECRET"),
            'grant_type': 'client_credentials'
        }
        response = requests.post("https://id.twitch.tv/oauth2/token", headers={'Content-Type': 'application/x-www-form-urlencoded'}, data=payload)
        token = json.loads(response.text)["access_token"]
        self.headers = {'Authorization': f'Bearer {token}', 'Client-Id': os.environ.get("TWITCH_CLIENT_ID")}

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
        file = ''.join(filter(str.isalpha, f'{clip["title"]}')) + ".mp4"
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
        import subprocess
        def get_length(filename):
            result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                    "format=duration", "-of",
                                    "default=noprint_wrappers=1:nokey=1", filename],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)
            return float(result.stdout)

        duration = get_length(path)

        #Slice video from last 3 seconds
        slicedPath = f'/app/files/clips/sliced{file}'

        from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
        startTime = (round(duration/100) * 20) #Cut the first 20 percent of the video
        endTime = round(duration - ((duration/100) * 20)) #Cut the last 20 percent of the video
        ffmpeg_extract_subclip(path, startTime, endTime, targetname=slicedPath)

        return slicedPath
    
    def is_video_long_enough(self, total_duration, duration):
        total_duration > duration
        
    def get_clips_from_streamer(self, streamer_name: str):
        clips_time = 0
        streamer_id = self.convert_name_to_id(streamer_name)
        if streamer_id == None:
            return
        url_clips = self.get_clips_url_from_streamer(streamer_id)
        for url in url_clips[:2]:
            clips_time += float(url["duration"])
            downloaded_clip = self.download_clip(url)
        return [clips_time, downloaded_clip]
    
    def download_clips_from_twitch(self, duration):
        paths = []
        popular_ordered_streamer_names = self.get_streamers()
        total_time = 0
        for streamer_name in popular_ordered_streamer_names:
            if self.is_video_long_enough(total_time, duration):
                break
            try:
                clips_time, downloaded_clips_paths = self.get_clips_from_streamer(
                    streamer_name)
                print(clips_time)
                total_time += clips_time
                paths.append(downloaded_clips_paths)
            finally:
                continue
        return paths
    
    def get_clips_url_from_streamer(self, id):
        '''Downloads the clips from a streamer from the twitch API, based also on timeframe, and sorted by views'''
        format_time = "%Y-%m-%dT%H:%M:%SZ"
        params = {
            "broadcaster_id": id,
            "started_at": (datetime.datetime.now() - datetime.timedelta(days=3)).strftime(format_time),
            "ended_at": datetime.datetime.now().strftime(format_time)
        }
        request = requests.get(
            f'https://api.twitch.tv/helix/clips', headers=self.headers, params=params)
        return json.loads(request.text)["data"]