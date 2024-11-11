import json
import logging
import time
from enum import Enum
from io import BytesIO
from uuid import uuid4

from PIL import Image
from requests import get
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from utils.globals import work_dir
from utils.mongo import get_unused_id


class Trend(Enum):
    RISING = "rising"
    NEW = "new"
    TOP = "top"
    HOT = "hot"


class Reddit:
    def __init__(self):
        pass

    def remove_element(self, driver, by: By, path):
        element = driver.find_element(by, path)
        driver.execute_script("""
            var element = arguments[0];
            element.parentNode.removeChild(element);
            """, element)

    def get_post_lists(self, subreddit, trend: Trend):
        while True:
            try:
                response = get(
                    f'''https://www.reddit.com/r/{subreddit}/{trend.value}/.json''', verify=False)
                if not response.ok:
                    raise Exception("Reddit resopnse not ok: ", response.content)
                data = json.loads(response.text)
                return data["data"]["children"]
            except Exception as e:
                print(f"Errore: {e}. Riprovo tra 10 secondi...")
                time.sleep(10)


    def get_screenshot_of_post(self, post_data, image_name):
        zoom = 3
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--width=6000")  # Set the desired width
        options.add_argument("--height=5000")  # Set the desired height
        options.add_argument('--disable-blink-features=AutomationControlled')
        driver = webdriver.Firefox(options=options)

        driver.get(post_data["url"])

        # Change theme to dark
        html = driver.find_element(By.XPATH, "/html")
        driver.execute_script("arguments[0].className = 'theme-dark';", html)
        driver.execute_script(
            "arguments[0].classList.remove('theme-light');", html)
        driver.implicitly_wait(5)

        # Remove back button
        self.remove_element(
            driver, By.XPATH, "/html/body/shreddit-app/div[1]/div[1]/div/main/shreddit-post/div[1]/span[1]/pdp-back-button")
        # Remove datestamp
        self.remove_element(
            driver, By.XPATH, "/html/body/shreddit-app/div[1]/div[1]/div/main/shreddit-post/div[1]/span[1]/div/span/faceplate-timeago/time")

        driver.execute_script(
            f"document.body.style.zoom = '{zoom * 100}%'")     # ZOOM

        # Crop to get the post only
        post_container = driver.find_element(By.CSS_SELECTOR, "#main-content")
        # Wrap words
        driver.execute_script("""
            var element = arguments[0];
            element.style.width = '8vw';
        """, post_container)

        post = driver.find_element(By.CSS_SELECTOR, "#" + post_data["name"])
        # Make screenshot
        screenshot = driver.get_screenshot_as_png()
        # Ricarica la posizione dell'elemento
        left = post.location['x']
        top = post.location['y']
        right = (post.location['x'] + post.size['width'])
        bottom = (post.location['y'] + post.size['height'])

        # Crop the image
        im = Image.open(BytesIO(screenshot))
        im = im.crop((left, top, right, bottom))
        im.save(image_name)
        driver.quit()

    def get_image(self, subreddit, trend: Trend):
        logging.info(f"Handling scraping reddit post: {subreddit}")
        
        posts = self.get_post_lists(subreddit, trend)
        target_dir = work_dir(f"{uuid4()}.png")
        
        post = get_unused_id({"source" : "reddit.com", "query": subreddit, "trend": trend.value}, posts, "url")
        
        self.get_screenshot_of_post(post["data"], target_dir)
        logging.info("Scraped reddit post: %s", target_dir)
        return target_dir, post["data"]["title"]
