import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time
import pickle
import os
import random
from  credentials import credentials

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_experimental_option("detach", True)
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
# driver = webdriver.Chrome(service=Service("./chromedriver"),options=options)
driver = webdriver.Chrome(options=options)
ERROR_COUNTER = 0

def login_process(driver):
    driver.get('https://www.linkedin.com/login/tr?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin/')
    time.sleep(5)
    driver.find_element(By.XPATH,'//*[@id="username"]').click()
    time.sleep(1.5)
    driver.find_element(By.XPATH,'//*[@id="username"]').send_keys(credentials()['username'])
    time.sleep(1.2)


    driver.find_element(By.XPATH, '//*[@id="password"]').click()
    time.sleep(1.1)

    driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(credentials()['password'])
    time.sleep(1.5)
    driver.find_element(By.XPATH, '//button[@aria-label="Oturum aç" and @type="submit"]').click()

    try:
        driver.find_element(By.XPATH,'//*[@id="ember26"]/button[1]').click()
    except:
        pass

def convert_string(string):
    return string.replace(' ','%20')

def connect_by_title(driver,title,page_count=3):
    for page in range(1,page_count+1):
        driver.get(f'https://www.linkedin.com/search/results/PEOPLE/?geoUrn=%5B"102890719"%5D&keywords={convert_string(title)}&origin=GLOBAL_SEARCH_HEADER&page={page}')
        time.sleep(10)
        all_people_ul = driver.find_element(By.XPATH, '//ul[@role="list" and contains(@class, "list-style-none")]')
        all_people_li = all_people_ul.find_elements(By.TAG_NAME,'li')

        for count,li in enumerate(all_people_li):
            for button in li.find_elements(By.TAG_NAME,'button'):
                if(button.text == "Follow"):
                    continue
                if('Connect' in button.text):
                    button.click()
                    time.sleep(2)
                    try:
                        popup_check = driver.find_elements(By.CLASS_NAME,'artdeco-button--primary')
                        for send_button in popup_check:
                            if('Send' in send_button.get_attribute('aria-label')):
                                send_button.click()
                                time.sleep(2) 
                    except:
                        pass
                    break
            try:
                p = driver.find_elements(By.CLASS_NAME,'artdeco-toast-item__message')[0]
                if("Unable to connect to" in p.text):
                    print("Unable to connect error occured")
                    time.sleep(5)

                    driver.find_elements(By.CLASS_NAME,'artdeco-toasts_toasts')[0].find_elements(By.TAG_NAME,'button')[0].click()
                    print("popup closed")
                    ERROR_COUNTER += 1
                    print(f"ERROR_COUNTER: {ERROR_COUNTER}")
                    if(ERROR_COUNTER == 5):
                        exit()

            except:
                pass
            
            time.sleep(random.randint(9,15))
        
            
        





if __name__ == "__main__":

    TITLE = "it recruiter remote"
    PAGE = 5

    if("cookies.pkl" in  os.listdir('.')):
        driver.get("https://linkedin.com")
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.get("https://linkedin.com")
    else:
        login_process(driver)
        pickle.dump(driver.get_cookies() , open("cookies.pkl","wb"))
    
    connect_by_title(driver,TITLE,page_count=PAGE)

    # bunu koyarsan her cikis yaparken cookie bilgisini kaydeder
    # pickle.dump(driver.get_cookies() , open("cookies.pkl","wb"))  
    driver.close()





