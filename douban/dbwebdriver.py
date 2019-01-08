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
    # '--headless',
    '--disable-gpu',
    'window-size=1024,768',
        '--no-sandbox'):
    options.add_argument(arg)

# Specify your own path to store and load cookies
COOKIE_FILE = "/usr/local/info/cookies.pkl"

def manual_login():
    # First login to store cookies
    print("📧 You have 30 seconds to login. Do NOT close chrome manually, it will exit automatically !!")
    url = "https://www.douban.com/login"
    driver = webdriver.Chrome()
    driver.get(url)
    try:
        element = WebDriverWait(
            driver, 30).until(
            EC.presence_of_element_located(
                (By.ID, "inp-query")))
        print("✔️  Login SUCCEED !")
        pickle.dump(driver.get_cookies(), open(COOKIE_FILE, "wb"))
    except Exception as e:
        print("☹️  Timeout. Try again and try quickly.")
        # raise e


def auto_login():
    '''
    :rtype: webdrive object
    '''
    if not os.path.exists(COOKIE_FILE):
        print(">> No cookie was found, you should login with Chrome-Browser for at least once.")
        manual_login()

    driver = webdriver.Chrome(options=options)    
    # This is necessary to let webdriver know which cookies is required
    douburl = "https://www.douban.com/login"
    driver.get(douburl)

    douburl = "https://www.douban.com"
    cookies = pickle.load(open(COOKIE_FILE, "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.get(douburl)
    time.sleep(3)
    return driver


def post_status(status):
    cont, images = '', []
    for item in status:
        if item.endswith(
                tuple(['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg'])):
            images.append(item)
        else:
            cont += ' ' + item

    driver = auto_login()
    status = driver.find_element_by_id('isay-cont')
    status.send_keys(cont)

    # uploads (at most 9) images,
    if len(images):
        upload = driver.find_element_by_id('isay-upload-inp')
        sz = 0
        for img in images:
            print(">> uploading", img, '...')
            upload.send_keys(str(os.path.realpath(img)))
            sz += os.path.getsize(img)
        # ESSENTIAL: wait for images-uploading completes, assuming
        # upload is 200KB/s, you might want to extend sleep time if your
        # network is slow.
        time.sleep(max(sz / (1024 * 200), 5))

    submit = driver.find_element_by_id('isay-submit')
    submit.send_keys(Keys.RETURN)
    print(">> post SUCCEED !")
    driver.quit()

    # element = driver.find_element_by_name("comment")
    # element.send_keys('Ash is purest black')
if __name__ == '__main__':
    post_status(sys.argv[1:])

