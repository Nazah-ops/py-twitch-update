import logging
import os

from dotenv import load_dotenv

from reddit import Reddit
from title import TitleGeneration
from twitch import Twitch
from video_editor import VideoEditor

""" from youtube import Youtube """

TOTAL_VIDEO_TIME = 1 * 60

logging.basicConfig(format="[%(asctime)s] - %(message)s", level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')


def main():
    logging.info('Inizio processo di scraping e upload.')

    load_dotenv("/app/keys/.env")
    twitch = Twitch()
    clips = twitch.download_clips_from_twitch(TOTAL_VIDEO_TIME)

    reddit = Reddit()
    reddit.get_image("TwoSentenceHorror")
    return
    video_editor = VideoEditor()
    video = video_editor.concat_fade(clips, transition_time=1)
    video_editor.add_intro_to_video(
        video, f'{os.environ.get("BASE_PATH")}/files/intro.mov')

    youtube_api = Youtube()
    youtube_api.upload(
        video_file=os.environ.get("OUTPUT"),
        title="Crack Highlight - League Of Legends #1",
        description="Follow me!",
        thumbnail_file=None)


main()

# NOTE TO SELF
# per convertire un AVI pesante per l'into a un mov -> ffmpeg -i Editor.avi -map 0 -c:v png -c:a copy output.mov
