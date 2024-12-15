import logging as logger
import ssl

from dotenv import load_dotenv

from utils.globals import clean_work_dir
from utils.make_reel import make_reel
from utils.mongo import close_mongo_client
from youtube import upload

""" from youtube import Youtube """

logger.basicConfig(format="[%(asctime)s] - %(message)s", level=logger.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')



def main():
    ssl._create_default_https_context = ssl._create_unverified_context # type: ignore
    logger.info('Inizio processo di scraping e upload.')
    load_dotenv("/app/keys/.env")

    clean_work_dir()
    video, title, keywords = make_reel()
    
    #if os.environ.get('ENV') == "PROD":
    upload(file=video, title=title, keywords=keywords)

    logger.info(f"Video produced: {title}")
 
    close_mongo_client()

main()

# NOTE TO SELF
# per convertire un AVI pesante per l'into a un mov -> ffmpeg -i Editor.avi -map 0 -c:v png -c:a copy output.mov
