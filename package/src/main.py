import json
import logging
import logging as logger
import os
from os.path import dirname, join

from dotenv import load_dotenv
# from face_model import FaceModel
from movie import VideoEditor
from twitch import TwitchAPI
from youtube import YoutubeAPI

# Loading environment variables
TOTAL_VIDEO_TIME = 1 * 60

logging.basicConfig(format="%(asctime)-15s %(message)s", level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')


def is_video_long_enough(total_duration):
    total_duration > TOTAL_VIDEO_TIME


def get_clips_from_streamer(streamer_name: str):
    twitch_api = TwitchAPI()
    clips_time = 0
    streamer_id = twitch_api.convert_name_to_id(streamer_name)
    if streamer_id == None:
        return

    url_clips = twitch_api.get_clips_url_from_streamer(streamer_id)

    for url in url_clips[:2]:
        clips_time += float(url["duration"])
        downloaded_clip = twitch_api.download_clip(url)

    return [clips_time, downloaded_clip]


def download_clips_from_twitch():
    paths = []
    popular_ordered_streamer_names = TwitchAPI.get_most_popular_streamers()
    total_time = 0

    for streamer_name in popular_ordered_streamer_names:

        if is_video_long_enough(total_time):
            break

        clips_time, downloaded_clips_paths = get_clips_from_streamer(
            streamer_name)
        total_time += clips_time
        paths = paths + downloaded_clips_paths

    return paths


def main():
    env_path = join(dirname(__file__), '.env')
    load_dotenv(env_path)

    video_editor = VideoEditor()

    local_paths_clips = download_clips_from_twitch()

    concat_clip = video_editor.concatenate_fade_video(
        local_paths_clips, transition_time=1)

    video_editor.add_intro_to_video(
        concat_clip, f'''{os.environ.get("BASE_PATH")}/files/intro.mov''')

    youtube_api = YoutubeAPI()
    youtube_api.upload_to_channel(video_path=os.environ.get(
        "OUTPUT"), title="Crack Highlight - League Of Legends #1", description="Follow me!", thumbnail_path=None)


main()


# TEST
'''import os
# movie.overlay_video("files/clips/bug.mp4","files/intro1.mov")
movie = Movie(transition_time=2)

# Get the list of all files and directories
path = "/app/files/clips/"
dir_list = os.listdir(path)
logger.info("Fading...")
movie.fade_all_video(dir_list)
'''
# NOTE TO SELF
# per convertire un AVI pesante per l'into a un mov -> ffmpeg -i Editor.avi -map 0 -c:v png -c:a copy output.mov
