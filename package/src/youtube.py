import time

import os
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Youtube:
    
    def __init__(self) -> None:
        return

    def click(self, driver, element):
        delay = 5 # seconds
        try:
            myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, element)))
            time.sleep(2)
            myElem.click()
        except TimeoutException:
            print ("Loading took too much time!")

    def upload(self, video_path, title, description, thumbnail_path):

        #Initializing the WebDriver
        profileFolder = '/app/files/profiles/youtube'
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        options.add_argument("-profile")
        options.add_argument(profileFolder)
        driver = webdriver.Firefox(options=options)

        #Refresh page to see the updated page
        driver.get("https://www.youtube.com/upload")

        #Inputing the file
        driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-uploads-file-picker/div/input').send_keys(video_path)
        
        time.sleep(5)

        #Title of the video
        title_element = driver.find_element(By.XPATH, '//*[@id="textbox"]')
        title_element.clear()
        title_element.send_keys(title)
        
        time.sleep(5)

        #Description of the video
        #Description of the video
        description_element = driver.find_element(By.CSS_SELECTOR, '#description-textarea > ytcp-form-input-container:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > ytcp-social-suggestion-input:nth-child(1) > div:nth-child(1)')
        description_element.clear()
        description_element.send_keys(description)
        
        time.sleep(5)

        #Thumbnail of the video
        #self.driver.find_element(By.XPATH, '//*[@id="select-button"]').send_keys('/app/files/thumbnail/g10IqBGyy8.png')
        
        #It's not made for kids
        self.click(driver, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[5]/ytkc-made-for-kids-select/div[4]/tp-yt-paper-radio-group/tp-yt-paper-radio-button[2]')
        
        #Next to video elements
        self.click(driver, '//*[@id="next-button"]')
        
        #Next to checks
        self.click(driver, '//*[@id="next-button"]')

        time.sleep(5)

        #Check copyright
        copyright_element = driver.find_element(By.XPATH, '//*[@id="results-description"]')
        if copyright_element.text != 'No issues found':
            print("mandare errore")
        
        time.sleep(5)


        #Next to visibility
        self.click(driver, '//*[@id="next-button"]')
        
        time.sleep(5)


        #Put on visible
        self.click(driver, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-uploads-review/div[2]/div[1]/ytcp-video-visibility-select/div[2]/tp-yt-paper-radio-group/tp-yt-paper-radio-button[3]')

        time.sleep(5)
        
        #Get video link
        #video_link = driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-uploads-review/div[3]/ytcp-video-info/div/div[2]/div[1]/div[2]/span/a').text
        
        time.sleep(5)

        #Publish
        self.click(driver, '//*[@id="done-button"]')