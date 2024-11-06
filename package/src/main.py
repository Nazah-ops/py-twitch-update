import logging

from dotenv import load_dotenv

from pexel import Orientation, Pexel
from reddit import Reddit
from sound import Sound
from title import TitleGeneration
from twitch import Twitch
from utils.globals import clean_work_dir
from video_editor import VideoEditor

""" from youtube import Youtube """

TOTAL_VIDEO_TIME = 1 * 60

logging.basicConfig(format="[%(asctime)s] - %(message)s", level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def main():
    logging.info('Inizio processo di scraping e upload.')

    load_dotenv("/app/keys/.env")

    clean_work_dir()
    
    sound = Sound()
    soundeffect = sound.download_sound("", "sinister")

    pexel = Pexel();
    pexel_video = pexel.get_video("dark", Orientation.PORTRAIT);
    
    reddit = Reddit()
    reddit_image = reddit.get_image("TwoSentenceHorror")
    
    
    video_editor = VideoEditor()
    video_with_image = video_editor.image_to_center(video=pexel_video, image=reddit_image)
    final_video = video_editor.merge_audio_with_video(video_with_image, soundeffect)
    
    print("Final result: ", final_video)
main()

# NOTE TO SELF
# per convertire un AVI pesante per l'into a un mov -> ffmpeg -i Editor.avi -map 0 -c:v png -c:a copy output.mov
