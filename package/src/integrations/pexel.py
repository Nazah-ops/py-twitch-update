import http.client
import json
import logging
from dataclasses import dataclass, is_dataclass
from enum import Enum
from typing import Any, List, Optional
from uuid import uuid4

from dacite import from_dict
from moviepy import video
from moviepy.editor import VideoFileClip

from utils.download import download
from utils.globals import work_dir
from utils.mongo import get_unused_id_dict


class Orientation(Enum):
    LANDSCAPE = "landscape"
    PORTRAIT = "portrait"
    SQUARE = "square"


@dataclass
class User:
    id: int
    name: str
    url: str


@dataclass
class VideoFile:
    id: int
    quality: str
    file_type: str
    width: int
    height: int
    fps: float
    link: str
    size: int


@dataclass
class VideoPicture:
    id: int
    nr: int
    picture: str


@dataclass
class Video:
    id: int
    width: int
    height: int
    duration: int
    full_res: Optional[str]
    tags: List[str]
    url: str
    image: str
    avg_color: Optional[str]
    user: User
    video_files: List[VideoFile]
    video_pictures: List[VideoPicture]

def get_video(topic: str,  orientation: Orientation) -> str:
    """ 
        Downloads a video from pexel given the topic, then returns the name of the video
    """
    logging.info(f"Handling download background video: {topic} {orientation}")
    video_list: list[Video] = get_video_query(topic,  orientation)
    video_meta_data: Video = get_unused_id_dict({"query": topic, "orientation": orientation.value, "source":"pexel.com"}, video_list,['url'])
    url = max(video_meta_data.video_files, key=lambda video: video.size).link
    
    video_name = work_dir(f"{uuid4()}.mp4")
    download(url, video_name)

    gray_name = work_dir(f"{uuid4()}.mp4")
    clip = VideoFileClip(video_name)
    gray_clip = video.fx.all.blackwhite(clip)
    gray_clip.write_videofile(gray_name)

    logging.info(f"Downloaded background video: {gray_name}")
    return gray_name

def get_video_query(topic: str,  orientation: Orientation) -> list[Video]:
    conn = http.client.HTTPSConnection("api.pexels.com")
    headers = {
        'Authorization': 'yL7ewVOVKa8nh1pR7koTTlntKO1IkNvWMoQRP4I0ANfFr0ev1F0mIAjo',
    }
    conn.request("GET", f"/videos/search?query={topic}&per_page=15&orientation={orientation.value}", {}, headers)
    data = conn.getresponse().read().decode("utf-8")
    videos = [from_dict(data_class=Video, data=video_dict) for video_dict in json.loads(data)["videos"]]
    return [video for video in videos if video.height >= 1920]

