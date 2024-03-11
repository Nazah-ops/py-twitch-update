from youtube import Youtube
import json
import logging
import logging as logger
import os
from os.path import join
from dotenv import load_dotenv

from face_model import FaceModel
from movie import Movie
from twitch import Twitch

# Loading environment variables
time = 8 * 60
output = "files/clips/final_output.mp4"

logging.basicConfig(format="%(asctime)-15s %(message)s", level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')


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

            video_time += float(clip["duration"])
            clips.append(downloaded_clip)
            # if (face_model.happy_video(downloaded_clip, 20)):

    return clips


def main():

    dotenv_path = join(os.path.abspath(os.curdir), '.env')
    load_dotenv(dotenv_path)

    logger.info("Starting Program")
    # Inizializzazione oggetto per concatenazione dei video
    movie = Movie(transition_time=1)

    logger.info("Downloading videos...")
    # Download dei video
    clips = download_batch_rank()

    print(clips)
    logger.info("Fading...")
    # Mette le transizioni per i video
    movie.fade_all_video(clips)

    # Mette la intro
    movie.overlay_video(output, "files/intro.mov")
    # TBD /app/files/output.mp4
    # TBD upload directly to youtube
    youtube = Youtube()
    youtube.upload(video_path=output, title= "Crack Highlight - League Of Legends #1", description="Follow me!", thumbnail_path=None)


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
