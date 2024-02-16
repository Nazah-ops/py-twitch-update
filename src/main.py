import json
import logging as logger

from twitch import Twitch
from movie import Movie
from face_model import FaceModel

import os
#Loading environment variables
time = 2 * 60

logger.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

def dump_json(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def download_batch_rank():
    face_model = FaceModel()
    twitch = Twitch()
    clips = []
    video_time = 0

    streamers = Twitch.get_streamers()

    for streamer in streamers:
        streamer_id = twitch.convert_name_to_id(streamer)
        
        if streamer_id == None:
            continue
        
        clips_downloaded = twitch.clips_from_broadcaster_id(streamer_id)[:3]
        if video_time > time:
            break
        for clip in clips_downloaded:
            downloaded_clip = twitch.download_clip(clip)
            if(face_model.happy_video(downloaded_clip, 20)):
                video_time += float(clip["duration"])
                clips.append(downloaded_clip)
           
    return clips


def main():
    movie = Movie(transition_time = 2)
    clips = download_batch_rank()
    Movie.fade_all_video(clips)
    movie.overlay_video("files/clips/final_output.mp4", "files/intro.mov")

    #TBD /app/files/output.mp4
    #TBD upload directly to youtube
    
main()