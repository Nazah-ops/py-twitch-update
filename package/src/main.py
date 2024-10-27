import argparse
import logging
import logging as logger
import os
from http import client
from os.path import dirname, join

from dotenv import load_dotenv
from reddit import Reddit
from title import TitleGeneration
from twitch import TwitchAPI
from video_editor import VideoEditor

from package.src.youtube import YoutubeAPI

# from face_model import FaceModel


""" from youtube import YoutubeAPI """

# Loading environment variables
TOTAL_VIDEO_TIME = 1 * 60

logging.basicConfig(format="[%(asctime)s] - %(message)s", level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')


def main():
    logging.info('Inizio processo di scraping e upload.')

    env_path = join(dirname(__file__), '.env')
    load_dotenv("/app/keys/.env")

    twitch = TwitchAPI()
    clips = twitch.download_clips_from_twitch()

    reddit = Reddit()
    reddit.get_image("TwoSentenceHorror")

    reddit.get_screenshot_of_post({
        "name": "t3_1gau18l",
        "url": "https://www.reddit.com/r/TwoSentenceHorror/comments/1gau18l/i_didnt_know_what_to_say_to_my_6_year_old_son/",
    }, "test.png")

    video_editor = VideoEditor()
    video = video_editor.concat_fade(clips, transition_time=1)
    video_editor.add_intro_to_video(
        video, f'{os.environ.get("BASE_PATH")}/files/intro.mov')

    youtube_api = YoutubeAPI()
    youtube_api.upload(
        video_file=os.environ.get("OUTPUT"),
        title="Crack Highlight - League Of Legends #1",
        description="Follow me!",
        thumbnail_file=None)


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
