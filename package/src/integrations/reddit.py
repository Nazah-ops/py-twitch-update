import json
import logging
import time
from dataclasses import dataclass, field
from enum import Enum
from io import BytesIO
from typing import Any, Dict, List, Optional, Union
from uuid import uuid4

from dacite import from_dict
from PIL import Image
from requests import get
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from utils.globals import work_dir
from utils.mongo import get_unused_id_dict


@dataclass
class MediaEmbed:
    content: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Data:
    approved_at_utc: Optional[float]
    subreddit: str
    selftext: str
    author_fullname: str
    saved: bool
    mod_reason_title: Optional[str]
    gilded: int
    clicked: bool
    title: str
    link_flair_richtext: List[str]
    subreddit_name_prefixed: str
    hidden: bool
    pwls: int
    link_flair_css_class: Optional[str]
    downs: int
    top_awarded_type: Optional[str]
    hide_score: bool
    name: str
    quarantine: bool
    link_flair_text_color: str
    upvote_ratio: float
    author_flair_background_color: Optional[str]
    subreddit_type: str
    ups: int
    total_awards_received: int
    media_embed: MediaEmbed
    author_flair_template_id: Optional[str]
    is_original_content: bool
    user_reports: List[Any]
    secure_media: Optional[Any]
    is_reddit_media_domain: bool
    is_meta: bool
    category: Optional[str]
    secure_media_embed: MediaEmbed
    link_flair_text: Optional[str]
    can_mod_post: bool
    score: int
    approved_by: Optional[Any]
    is_created_from_ads_ui: bool
    author_premium: bool
    thumbnail: str
    edited: Optional[Union[bool, float]]
    author_flair_css_class: Optional[str]
    author_flair_richtext: List[Any]
    gildings: Dict[str, int]
    content_categories: Optional[Any]
    is_self: bool
    mod_note: Optional[str]
    created: float
    link_flair_type: str
    wls: int
    removed_by_category: Optional[Any]
    banned_by: Optional[Any]
    author_flair_type: str
    domain: str
    allow_live_comments: bool
    selftext_html: Optional[str]
    likes: Optional[Any]
    suggested_sort: Optional[Any]
    banned_at_utc: Optional[Any]
    view_count: Optional[Any]
    archived: bool
    no_follow: bool
    is_crosspostable: bool
    pinned: bool
    over_18: bool
    all_awardings: List[Any]
    awarders: List[Any]
    media_only: bool
    can_gild: bool
    spoiler: bool
    locked: bool
    author_flair_text: Optional[str]
    treatment_tags: List[str]
    visited: bool
    removed_by: Optional[Any]
    num_reports: Optional[Any]
    distinguished: Optional[Any]
    subreddit_id: str
    author_is_blocked: bool
    mod_reason_by: Optional[Any]
    removal_reason: Optional[Any]
    link_flair_background_color: str
    id: str
    is_robot_indexable: bool
    report_reasons: Optional[Any]
    author: str
    discussion_type: Optional[Any]
    num_comments: int
    send_replies: bool
    contest_mode: bool
    mod_reports: List[Any]
    author_patreon_flair: bool
    author_flair_text_color: Optional[str]
    permalink: str
    stickied: bool
    url: str
    subreddit_subscribers: int
    created_utc: float
    num_crossposts: int
    media: Optional[Any]
    is_video: bool

@dataclass
class RedditPost:
    kind: str
    data: Data

class Trend(Enum):
    RISING = "rising"
    NEW = "new"
    TOP = "top"
    HOT = "hot"


class RedditClient:
    def __init__(self):
        pass

    def remove_element(self, driver, by: By, path):
        element = driver.find_element(by, path)
        driver.execute_script("""
            var element = arguments[0];
            element.parentNode.removeChild(element);
            """, element)

    def get_post_lists(self, subreddit, trend: Trend) -> list[RedditPost]:
        while True:
            try:
                response = get(
                    f'''https://www.reddit.com/r/{subreddit}/{trend.value}/.json''', verify=False)
                if not response.ok:
                    raise Exception("Reddit response not ok: ", response.content)
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
        
        posts: list[RedditPost] = self.get_post_lists(subreddit, trend)
        target_dir = work_dir(f"{uuid4()}.png")
        post: RedditPost = get_unused_id_dict({"source" : "reddit.com", "query": subreddit, "trend": trend.value}, posts, "url")
        
        self.get_screenshot_of_post(post["data"], target_dir)
        logging.info("Scraped reddit post: %s", target_dir)
        return target_dir, post["data"]["title"]