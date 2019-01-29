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
import random
from bs4 import BeautifulSoup

options = Options()
for arg in (
    '--headless',
    '--disable-gpu',
    'window-size=1024,768',
    '--no-sandbox',
    '--disable-dev-shm-usage'):
    options.add_argument(arg)

# Specify your own path to store and load cookies
COOKIE_FILE = "/usr/local/info/douban.pkl"

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
    driver.maximize_window()
    time.sleep(0.5)
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

def fake_rating_num(r):
    if r <= 4:
        return 1
    elif r <= 6:
        return 2
    elif r <= 8:
        return 3
    elif r <= 9:
        return 4
    else:
        return 5



def rate_movie(rate, url):
    # rate \in [1, 5]
    driver = auto_login()
    driver.get(url)
    if '我看过这部电影' in driver.page_source: 
        driver.quit()
        return 

    copied_reply = driver.find_element_by_class_name('short').text
    rate_num = driver.find_element_by_class_name('rating_num').text
    rate_num = fake_rating_num(float(rate_num))
    print(rate_num)

    driver.find_elements_by_class_name('collect_btn')[1].click()
    time.sleep(0.5)
    # print(driver.page_source)

    stars = 'star' + str(rate_num)
    driver.find_element_by_id(stars).click()    
    driver.find_element_by_id('comment').click()
    driver.find_element_by_id('comment').send_keys(copied_reply)
    driver.find_element_by_id('share-shuo').click()
    # driver.find_element_by_xpath("//input[@name='save']").click()
    time.sleep(5)

    driver.quit()


def delete_status():
    # delete by tag 
    page =  'https://www.douban.com/people/cactus207/statuses'
    driver = auto_login()
    pageid = 8
    while pageid < 15:
        driver.get(page + "?p=" + str(pageid))
        ids = [] 
        for idx, div in enumerate(BeautifulSoup(driver.page_source, 'lxml').findAll('div', {"class": "status-saying"})):
            if '#Nature#' in div.text or '#Feelings#' in div.text or '#Paris#' in div.text:
                ids.append(idx)

        ss = driver.find_elements_by_class_name('btn-action-reply-delete')
        for idx in ids:
            try:
                ss[idx].click()
                time.sleep(0.3)
                alert = driver.switch_to.alert
                alert.accept()
                time.sleep(random.randint(1,3))
                # time.sleep(0.5)
            except Exception as e:
                print(e)

        time.sleep(1)
        driver.get(page + "?p=" + str(pageid))
        page_source = driver.page_source
        if any([tag in page_source for tag in ('#Nature#', '#Feelings#', '#Paris#')]):
            pageid -= 1
        else:
            pageid += 1

    time.sleep(2)
    driver.quit()


if __name__ == '__main__':
    post_status(sys.argv[1:])
    url = 'https://movie.douban.com/subject/25937991/?from=showing'
    url = 'https://movie.douban.com/subject/26425063/?tag=%E7%83%AD%E9%97%A8&from=gaia_video'
    url = 'https://movie.douban.com/subject/30157153/?tag=%E7%83%AD%E9%97%A8&from=gaia'
    # rate_movie(3, url)
    # delete_status()

