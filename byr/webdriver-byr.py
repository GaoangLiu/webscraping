from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pickle
import time
import sys
import os
import re

options = Options()
for arg in (
    '--headless',
    '--disable-gpu',
    'window-size=1024,768',
    '--no-sandbox',
    'disable-infobars'):
    options.add_argument(arg)

# Specify your own path to store and load cookies
COOKIE_FILE = "/usr/local/info/byrcookies.pkl"

def manual_login():
    # First login to store cookies
    print("📧 You have 30 seconds to login. Do NOT close chrome manually, it will exit automatically !!")
    url = "http://bt.byr.cn/login.php"
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    try:
        # element = WebDriverWait(
        #     driver, 30).until(
        #     EC.presence_of_element_located(
        #         (By.ID, "note_post")))
        time.sleep(15)
        print("✔️  Login SUCCEED !")
        pickle.dump(driver.get_cookies(), open(COOKIE_FILE, "wb"))
    except Exception as e:
        print("☹️  Timeout. Try again and try quickly.")
        # raise e
    driver.quit()


def auto_login():
    '''
    :rtype: webdrive object
    '''
    if not os.path.exists(COOKIE_FILE):
        print(">> No cookie was found, you should login with Chrome-Browser for at least once.")
        manual_login()
    
    driver = webdriver.Chrome(options=options)    
    # This is necessary to let webdriver know which cookies is required
    login_url = "http://bt.byr.cn"
    driver.get(login_url)

    main_url = login_url
    cookies = pickle.load(open(COOKIE_FILE, "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    ele = driver.get(main_url)
    print(driver.page_source)
    # ele.send_keys(Keys.RETURN)
    driver.quit()


import requests 
from bs4 import BeautifulSoup
import re
from urllib.request import urlretrieve

def login():
    session = requests.Session()
    # html = session.get("http://bt.byr.cn")
    mainpage = 'http://bt.byr.cn/'
    html = open("pagesource.html", 'rb').read()
    soup = BeautifulSoup(html, 'lxml')
    for link in soup.findAll('a', href=re.compile("^download*")) :
        down = link.attrs['href']
        print(session.get('http://bt.byr.cn/'+ down))
        urlretrieve(mainpage + down, "a.torrent")
        break


# auto_login() 
login()





