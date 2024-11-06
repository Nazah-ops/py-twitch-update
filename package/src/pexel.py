import http.client
import json
import logging
from uuid import uuid4
from enum import Enum
from utils.download import download
from utils.globals import work_dir

class Orientation(Enum):
    LANDSCAPE = "landscape"
    PORTRAIT = "portrait"
    SQUARE = "square"

class Pexel:
    def __init__(self):
        pass


    def get_video(self, topic,  orientation: Orientation):
        """ 
            Downloads a video from pexel given the topic, then returns the name of the video
        """
        logging.info(f"Handling download background video: {topic} {orientation}")
        videos = self.get_video_query(topic,  orientation)
        # Supponiamo che 'videos' sia una lista di dizionari come nel tuo esempio
        filtered_videos = filter(
            lambda video: video["height"] >= 1920 and any(
                video_file["height"] >= 1920 for video_file in video["video_files"]
            ),
            videos
        )

        # Estrai gli URL dei video che soddisfano i criteri
        url = [video_file["link"] for video in filtered_videos for video_file in video["video_files"] if video_file["height"] >= 1920][0]
        video_name = work_dir(f"{uuid4()}.mp4")
        download(url, video_name)
        logging.info(f"Downloaded background video: {video_name}")
        return video_name
    
    def get_video_query(self, topic,  orientation: Orientation):
        conn = http.client.HTTPSConnection("api.pexels.com")
        headers = {
            'Authorization': 'yL7ewVOVKa8nh1pR7koTTlntKO1IkNvWMoQRP4I0ANfFr0ev1F0mIAjo',
        }
        conn.request("GET", f"/videos/search?query={topic}&per_page=5&orientation={orientation.value}", {}, headers)
        data = conn.getresponse().read().decode("utf-8")
        print(json.loads(data))
        return json.loads(data)["videos"]
                        
