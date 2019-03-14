import os
import requests
import subprocess
import sys
import pickle
import json
from requests.auth import AuthBase, HTTPBasicAuth
from urllib.request import urlretrieve, urlopen
from bs4 import BeautifulSoup
from PIL import Image
from PIL import ImageOps
from ocr import OCR
from termcolor import colored

COOKIE_PATH = "/usr/local/info/dbcookie.dat"

class Douban:
    def __init__(self):
        ''' Two cases: 1. this account was logged in before before, a cookie file was created
        2. there is no such cookie file
        '''
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
        self.mainpage = "https://www.douban.com"

    def is_login(self):
        ''' Login or not, two cases to consider:
        1. this account was logged in before before, a cookie file was created;
        2. there is no such cookie file  .
        return False if there is no cookie or cookie is no more valid,
        otherwise return the session
        '''
        if not os.path.exists(COOKIE_PATH):
            return False

        self.session.cookies.update(pickle.load(open(COOKIE_PATH, 'rb')))
        r_get = self.session.get(self.mainpage)
        soup = BeautifulSoup(r_get.text, 'lxml')
        return 'UPLOAD_AUTH_TOKEN' in soup.text

    def save_cookies_login(self):
        ''' Log in account and localize cookies for further explorations.
        '''
        if self.is_login():
            print("🕷  COOKIE remains VALID. LOGIN", colored('SUCCESS!', 'green'))
            return
        else:
            print("🕷  COOKIE is INVALID", colored('FAILED', 'red'))            

        dhost = "http://www.douban.com/login"
        r_get = requests.get(dhost)
        bs_get = BeautifulSoup(r_get.text, 'lxml')

        captcha_solution = self.rec_captcha(
            bs_get.find("img", {"id": "captcha_image"}))
        cid = bs_get.find("input", {"name": "captcha-id"})
        captcha_id = cid['value'] if cid else None
        account = json.load(open('/usr/local/info/douban.json', 'r'))

        params = {
            'form_email': account['email'],
            'form_password': account['password'],
            'captcha-solution': captcha_solution,
            'captcha-id': captcha_id}
        print(params)

        s = self.session.post("https://accounts.douban.com/login", data=params)
        soup = BeautifulSoup(s.text, features="lxml")
        # print(soup.text)

        if 'UPLOAD_AUTH_TOKEN' in soup.text:
            print("Login SUCCESS!")
            # save cookies to local
            with open(COOKIE_PATH, 'wb') as f:
                pickle.dump(self.session.cookies, f)
        return

    def rec_captcha(self, captcha_items):
        ''' recognize captcha, either automatically or manually.
        '''
        if captcha_items:
            image_path = "images/captcha.jpg"
            urlretrieve(captcha_items['src'], image_path)
            return OCR().process_image(image_path)
        else:
            print("🕷 There is no captcha for this login page.")


    def post_status(self, content):
        ''' For now, only pure text status is support
        '''
        self.save_cookies_login()
        ck_value = self.session.cookies['ck']
        # files = {'media': open('images/captcha.jpg', 'rb').read()}
        # img=open('images/captcha.jpg', 'rb').read()
        self.session.post(
            self.mainpage,
            data={
                'ck': ck_value,
                'comment': content})
        print("🐜 status posted successfully.")

    def postMedia(self, text, images):
        self.save_cookies_login()
        s = self.session
        ck_value = s.cookies['ck']

        import re
        upload_auth_token = re.findall(r'UPLOAD_AUTH_TOKEN:\s*\"(.*)\"', str(BeautifulSoup(s.get(self.mainpage).text, 'lxml')))
        imgurls = []
        for i in images:
            res = s.post('https://www.douban.com/j/upload', data={'ck':ck_value, 'upload_auth_token':upload_auth_token}, files={"image":open(i, 'rb')})
            url = json.loads(BeautifulSoup(res.text, 'lxml').find('p').text)['url']
            imgurls.append(url)
        res = self.session.post(self.mainpage, data={'ck':ck_value, 'comment':text, 'uploaded':imgurls})
        soup = BeautifulSoup(res.text, 'lxml')
        print('status with media was SUCCESSFULLY posted.')


if __name__ == '__main__':
    db = Douban()

    # db.postMedia("再来几张高清壁纸..........", ['house.jpg', 'tur.jpg', 'res.jpg'])













