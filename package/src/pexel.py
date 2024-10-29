import http.client
import json
import uuid
from enum import Enum
from utils.download import download

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
        url = self.get_video_query(topic,  orientation)[0]["video_files"][0]["link"]
        video_name = f"/app/files/{uuid.uuid4().hex[:6].upper()}.mp4"
        download(url, video_name)
        return video_name
    def get_video_query(self, topic,  orientation: Orientation):
        conn = http.client.HTTPSConnection("api.pexels.com")
        headers = {
            'Authorization': 'yL7ewVOVKa8nh1pR7koTTlntKO1IkNvWMoQRP4I0ANfFr0ev1F0mIAjo',
        }
        conn.request("GET", f"/videos/search?query={topic}&per_page=5&orientation={orientation.value}", {}, headers)
        data = conn.getresponse().read().decode("utf-8")
        return json.loads(data)["videos"]
                        
