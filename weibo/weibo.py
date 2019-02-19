from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
# from bs4 import BeautifulSoup
import pickle
import time
import sys
import os
import re
import json 
import random 
import faker


class Weibo():
    def __init__(self):
        self.mainpage = 'https://weibo.com'
        self.hotpage = 'https://d.weibo.com/102803'
        self.ckfile = 'weibo.pkl'

    def initDriver(self):
        options = Options()
        # options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(options=options)

    def loginFromCookie(self):
        if not os.path.exists(self.ckfile): return False 
        self.driver.get(self.mainpage)
        for cookie in pickle.load(open(self.ckfile, "rb")):
            self.driver.add_cookie(cookie)
        self.driver.get(self.mainpage)
        return "我的首页" in self.driver.page_source


    def login(self):
        self.initDriver()        
        if self.loginFromCookie(): return 

        self.driver.get(self.mainpage)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'W_input')))            
        self.driver.find_elements_by_class_name('W_input')[1].clear()
        self.driver.find_elements_by_class_name('W_input')[1].send_keys('0012344072558')
        self.driver.find_elements_by_class_name('W_input')[2].send_keys('weibo@2019')
        self.driver.find_elements_by_class_name('W_input')[2].send_keys(Keys.RETURN)         
        time.sleep(10)
        pickle.dump(self.driver.get_cookies(), open(self.ckfile, "wb"))

    def postStatus(self, text, images=[]):
        self.driver.find_elements_by_class_name('W_input')[1].send_keys(text)
        upload = self.driver.find_element_by_xpath("//input[@name='pic1']")
        sz = 0
        for img in images[0:9]:
            print("UPLOADING", img, '...')
            upload.send_keys(str(os.path.realpath(img)))
            sz += os.path.getsize(img)
        time.sleep(max(sz / (1024 * 200), 5))
        self.driver.find_element_by_class_name('W_btn_a').click()

    def tearDown(self):
        if self.driver: self.driver.quit()

    def waterFeeds(self):
        wid = random.randint(1, 10)
        self.driver.get(self.hotpage)
        time.sleep(1)
        core = random.choice(['24小时', '1小时', '周榜', '月榜', '男榜', '女榜'])

        self.driver.find_element_by_partial_link_text(core).click()
        self.driver.set_window_size(1024, 30000)
        time.sleep(3)

        self.driver.find_elements_by_xpath("//span[@node-type='comment_btn_text']")[wid].click()
        time.sleep(1)
        feed = self.driver.find_elements_by_class_name("WB_text")[wid+1].text

        # fakename = ''.join(faker.Faker().name().split())
        nickname = self.driver.find_elements_by_class_name('WB_info')[wid].text
        feed = '/'.join(feed.split('：')[1:]) + ' @' + nickname
        print(wid, feed)
        # print(self.driver.page_source)   
        time.sleep(2)
        self.driver.find_elements_by_class_name('W_input')[1].send_keys(feed)
        self.driver.find_element_by_partial_link_text('评论').click()


    def safeWaterFeeds(self, n=10):
        for _ in range(n):
            try:
                self.waterFeeds()
            except Exception as e:
                print(e)


if __name__ == '__main__':
    images = ['404.jpg', 'test.jpg']
    wb = Weibo()
    wb.login()
    wb.safeWaterFeeds(5)
    # wb.waterFeeds()
    wb.tearDown()



