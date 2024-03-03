import json
import time

import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Youtube:
    
    def __init__(self) -> None:
        #Credentials
        self.username = "testingbruh67@gmail.com"
        self.password = "e#A6uNfEfU9]t3>"
    
        #Initializing the WebDriver
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Firefox(chrome_options)

    def updateCookies(self):
        session = requests.Session()

        #Set the current cookies
        with open('/app/files/cookies.json', 'r') as f:
            cookies = requests.utils.cookiejar_from_dict(json.load(f))
            session.cookies.update(cookies)
        
        #Get to the page
        response = session.get('https://yt3.ggpht.com/w5IAgRMeI1B4bS1lvtt3UJXQw20yJ85LxyuDKiTEWjCCXK-HmgfF7o1DEoyyIny8bnA2bL9Tp3E=s88-c-k-c0x00ffffff-no-rj')
        print(response.status_code)
        
        if response.status_code == 200:
            with open('/app/files/test.jpg', 'wb') as f:
                f.write(response.content)


        # Get the new cookies
        with open('/app/files/cookies.json', 'w') as f:
            json.dump(requests.utils.dict_from_cookiejar(session.cookies), f)

        with open('/app/files/test.html', 'w') as f:
            f.write(session.get('http://www.youtube.com').text)

    def click(self, element):
        delay = 5 # seconds
        try:
            myElem = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, element)))
            time.sleep(2)
            myElem.click()
        except TimeoutException:
            print ("Loading took too much time!")
        self.driver.save_screenshot("test.png")

    def upload(self, video_path, title, description, thumbnail_path):
        self.updateCookies()
        self.driver.get("https://www.youtube.com/")
        self.driver.delete_all_cookies()

        #Add cookies to the website
        with open("/app/files/cookies.json") as file:
            for key, value in json.load(file).items():
                self.driver.add_cookie({"name": key, "value": value})

        self.driver.get("https://www.youtube.com/")
        time.sleep(15)

        #Updates the cookies stored in the local json
        with open("/app/files/cookies.json", 'w') as file:
            file.write(json.dumps(self.driver.get_cookies()))


        #Refresh page to see the updated page
        self.driver.get("https://www.youtube.com/upload")
        self.driver.save_screenshot("test.png")

        time.sleep(8)
        self.driver.save_screenshot("test.png")

        #Passa a youtube studio
        self.driver.find_element(By.XPATH, '/html/body/div/div[5]/a').click()
        self.driver.save_screenshot("test.png")

        #Inputing the file
        self.driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-uploads-file-picker/div/input').send_keys(video_path)
        
        time.sleep(5)

        #Title of the video
        title_element = self.driver.find_element(By.XPATH, '//*[@id="textbox"]')
        title_element.clear()
        title_element.send_keys(title)
        
        time.sleep(5)

        #Description of the video
        description_element = self.driver.find_element(By.XPATH, '//*[@id="textbox"]')
        description_element.clear()
        description_element.send_keys(description)
        
        time.sleep(5)

        #Thumbnail of the video
        #self.driver.find_element(By.XPATH, '//*[@id="select-button"]').send_keys('/app/files/thumbnail/g10IqBGyy8.png')
        
        #It's not made for kids
        self.click('/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[5]/ytkc-made-for-kids-select/div[4]/tp-yt-paper-radio-group/tp-yt-paper-radio-button[2]')
        
        #Next to video elements
        self.click('//*[@id="next-button"]')
        
        #Next to checks
        self.click('//*[@id="next-button"]')

        time.sleep(5)

        #Check copyright
        copyright_element = self.driver.find_element(By.XPATH, '//*[@id="results-description"]')
        copyright_element = self.driver.find_element(By.XPATH, '//*[@id="results-description"]')
        if copyright_element.text != 'No issues found':
            print("mandare errore")
        
        time.sleep(5)


        #Next to visibility
        self.click('//*[@id="next-button"]')
        
        time.sleep(5)


        #Put on visible
        self.click('/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-uploads-review/div[2]/div[1]/ytcp-video-visibility-select/div[2]/tp-yt-paper-radio-group/tp-yt-paper-radio-button[3]')

        time.sleep(5)
        
        #Get video link
        video_link = self.driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-uploads-review/div[3]/ytcp-video-info/div/div[2]/div[1]/div[2]/span/a').text
        
        time.sleep(5)

        #Publish
        self.click('//*[@id="done-button"]')