from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import FirefoxOptions
import time

class Youtube:
    
    def __init__(self) -> None:
        #Credentials
        self.username = "testingbruh67@gmail.com"
        self.password = "e#A6uNfEfU9]t3>"
    
    def sleep():
        time.sleep(3)
    
    def upload(self, video_path, title, description, thumbnail_path):
        opts = FirefoxOptions()
        opts.add_argument("--headless")

        driver = webdriver.Firefox(options=opts)
        driver.get("https://www.youtube.com/")
        
        self.sleep()
        
        #Rejecting the privacy window
        driver.find_element(By.XPATH, "/html/body/ytd-app/ytd-consent-bump-v2-lightbox/tp-yt-paper-dialog/div[4]/div[2]/div[6]/div[1]/ytd-button-renderer[1]/yt-button-shape/button").click()
        
        self.sleep()
        
        #Clicking the sign in
        driver.find_element(By.XPATH, "/html/body/ytd-app/div[1]/div/ytd-masthead/div[4]/div[3]/div[2]/ytd-button-renderer").click()
        
        self.sleep()
        
        #Digiting the mail
        digiting_mail = driver.find_element(By.XPATH, '//*[@id="identifierId"]')
        digiting_mail.send_keys(username)
        
        #Clicking next
        driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[2]/div/div[1]/div/div/button').click()
        
        #Digiting the password
        digiting_password = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[1]/div/form/span/section[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input')
        digiting_password.send_keys(password)
        
        #Clicking next
        driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[2]/div/div[1]/div/div/button').click()
        
        #Create
        driver.find_element(By.XPATH, '/html/body/ytd-app/div[1]/div/ytd-masthead/div[4]/div[3]/div[2]/ytd-topbar-menu-button-renderer[1]/div/a/yt-icon-button/button/yt-icon/yt-icon-shape/icon-shape/div').click()
        
        #Upload
        driver.find_element(By.XPATH, '/html/body/ytd-app/ytd-popup-container/tp-yt-iron-dropdown/div/ytd-multi-page-menu-renderer/div[3]/div[1]/yt-multi-page-menu-section-renderer/div[2]/ytd-compact-link-renderer[1]/a/tp-yt-paper-item').click()
        
        #Inputing the file
        driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-uploads-file-picker/div/input').send_keys("/app/files/clips/BOMBA.mp4")
        
        #Title of the video
        title_element = driver.find_element(By.XPATH, '//*[@id="textbox"]')
        title_element.clear()
        title_element.send_keys(title)
        
        #Description of the video
        description_element = driver.find_element(By.XPATH, '//*[@id="textbox"]')
        description_element.clear()
        description_element.send_keys(description)
        
        #Thumbnail of the video
        driver.find_element(By.XPATH, '//*[@id="select-button"]').send_keys('/app/files/thumbnail/g10IqBGyy8.png')
        
        #It's not made for kids
        driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[5]/ytkc-made-for-kids-select/div[4]/tp-yt-paper-radio-group/tp-yt-paper-radio-button[2]').click()
        
        #Next to video elements
        driver.find_element(By.XPATH, '//*[@id="next-button"]').click()
        
        #Next to checks
        driver.find_element(By.XPATH, '//*[@id="next-button"]').click()

        #Check copyright
        copyright_element = driver.find_element(By.XPATH, '//*[@id="results-description"]')
        copyright_element = driver.find_element(By.XPATH, '//*[@id="results-description"]')
        if copyright_element.text != 'No issues found':
            print("mandare errore")
            
        #Next to visibility
        driver.find_element(By.XPATH, '//*[@id="next-button"]').click()
        
        #Put on visible
        driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-uploads-review/div[2]/div[1]/ytcp-video-visibility-select/div[2]/tp-yt-paper-radio-group/tp-yt-paper-radio-button[3]').click()
        
        #Get video link
        video_link = driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-uploads-review/div[3]/ytcp-video-info/div/div[2]/div[1]/div[2]/span/a').text
        
        #Publish
        driver.find_element(By.XPATH, '//*[@id="done-button"]').click()