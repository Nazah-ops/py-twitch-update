import json
from io import BytesIO

from PIL import Image
from requests import get
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


class Reddit:
    def __init__(self):
        pass
    
    def driver_remove_element(self, driver, xpath):
        element = driver.find_element(By.XPATH, xpath)
        driver.execute_script("""
            var element = arguments[0];
            element.parentNode.removeChild(element);
            """, element)
        
    def get_post_lists(self, subreddit):
        response = get(f'''https://www.reddit.com/r/{subreddit}/rising/.json''')
        data = json.loads(response.text)
        return data["data"]["children"]
    
    def get_screenshot_of_post(self, post_data, image_name):
        options = Options()
        options.add_argument("--headless")
        options.add_argument('--disable-blink-features=AutomationControlled')
        driver = webdriver.Firefox(options=options)

        driver.get(post_data["url"])

        # Change theme to dark
        html = driver.find_element(By.XPATH, "/html")
        driver.execute_script(f"arguments[0].className = 'theme-dark';", html)
        driver.execute_script("arguments[0].classList.remove('theme-light');", html)
        driver.implicitly_wait(5)

        #Remove back button
        self.driver_remove_element(driver, "/html/body/shreddit-app/div[1]/div[1]/div/main/shreddit-post/div[1]/span[1]/pdp-back-button")
        #Remove datestamp
        self.driver_remove_element(driver, "/html/body/shreddit-app/div[1]/div[1]/div/main/shreddit-post/div[1]/span[1]/div/span/faceplate-timeago/time")
        
        #Make screenshot
        screenshot = driver.get_screenshot_as_png()

        #Crop to get the post only
        post = driver.find_element(By.CSS_SELECTOR, "#" + post_data["name"])
        left = post.location['x']
        top = post.location['y']
        right = post.location['x'] + post.size['width']
        bottom = post.location['y'] + post.size['height']

        #Crop the image
        im = Image.open(BytesIO(screenshot))
        im = im.crop((left, top, right, bottom))
        im.save(image_name)
        driver.quit()
        
    def get_image(self, subreddit):
        posts = self.get_post_lists(subreddit)
        self.get_screenshot_of_post(posts[0]["data"], "test.png")