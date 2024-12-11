import logging
import os
import ssl

from dotenv import load_dotenv

from utils.globals import clean_work_dir
from utils.make_reel import make_reel
from utils.mongo import close_mongo_client
from youtube import upload

""" from youtube import Youtube """

logging.basicConfig(format="[%(asctime)s] - %(message)s", level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')

ssl._create_default_https_context = ssl._create_unverified_context


def main():
    logging.info('Inizio processo di scraping e upload.')
    load_dotenv("/app/keys/.env")

    clean_work_dir()
    video, title = make_reel()
    
    if os.environ.get('ENV') == "PROD":
        upload(video, title)

    logging.info(f"Video produced: {video}")
 
    close_mongo_client()

main()

# NOTE TO SELF
# per convertire un AVI pesante per l'into a un mov -> ffmpeg -i Editor.avi -map 0 -c:v png -c:a copy output.mov
