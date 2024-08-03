import datetime
import json
import os
from os.path import dirname, join

import requests
from bs4 import BeautifulSoup


class TwitchAPI:

    def __init__(self):
        payload = {
            'client_id': os.environ.get('CLIENT_ID'),
            'client_secret': os.environ.get("CLIENT_SECRET"),
            'grant_type': 'client_credentials'
        }
        response = requests.post("https://id.twitch.tv/oauth2/token", headers={
                                 'Content-Type': 'application/x-www-form-urlencoded'}, data=payload)
        data = json.loads(response.text)
        if 'access_token' in data:
            token = json.loads(response.text)["access_token"]
            self.headers = {'Authorization': f'Bearer {token}',
                            'Client-Id': os.environ.get("CLIENT_ID")}
        else:
            raise Exception("Token not in data: " +
                            (response.text) + ", with payload: " + str(payload))

    @staticmethod
    def get_most_popular_streamers():
        '''
        Retreive from a third party website the list of the most watched streamers, the first 100
        Returns a list of strings
        '''
        results = []
        request = requests.get(
            'https://www.twitchmetrics.net/channels/viewership?game=League+of+Legends&lang=en&page=1')
        parsed_html = BeautifulSoup(request.text, features="html.parser")

        for name in parsed_html.body.find_all('h5', attrs={'class': 'mr-2 mb-0'}):
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

        params = {"login": "".join(name.split())}
        request = requests.get(
            f'https://api.twitch.tv/helix/users', headers=self.headers, params=params)
        if request.ok:
            return json.loads(request.text)["data"][0]["id"]
        else:
            raise Exception(f'Error from twitch endpoint {request.text}')

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

    def download_clip(self, clip):
        from pathlib import Path
        file = ''.join(filter(str.isalpha, f'{clip["title"]}')) + ".mp4"
        path = str(Path(dirname(__file__)).parent.absolute()) + \
            "/files/clips/" + file

        index = clip["thumbnail_url"].find('-preview')
        clip_url = clip["thumbnail_url"][:index] + '.mp4'
        r = requests.get(clip_url)

        if r.headers['Content-Type'] != 'binary/octet-stream':
            raise Exception(
                f'Failed to download clip from thumb: {clip["thumbnail_url"]}')

        if not os.path.exists('files/clips'):
            os.makedirs('files/clips')

        with open(path, 'wb') as f:
            f.write(r.content)

        # Get video length
        import subprocess

        def get_length(filename):
            result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                    "format=duration", "-of",
                                     "default=noprint_wrappers=1:nokey=1", filename],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
            return float(result.stdout)

        duration = get_length(path)

        # Slice video from last 3 seconds
        slicedPath = f'{os.environ.get("BASE_PATH")}/files/clips/sliced{file}'

        from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

        # Cut the first 20 percent of the video
        startTime = (round(duration/100) * 20)
        # Cut the last 20 percent of the video
        endTime = round(duration - ((duration/100) * 20))
        ffmpeg_extract_subclip(path, startTime, endTime, targetname=slicedPath)

        return slicedPath
