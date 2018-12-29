import os
import requests
from requests.auth import AuthBase, HTTPBasicAuth
from urllib.request import urlretrieve, urlopen
from bs4 import BeautifulSoup
import subprocess
from PIL import Image
from PIL import ImageOps
import sys
from ocr import OCR
import pickle
import json


class Douban:
    def __init__(self):
        ''' Two cases: 1. this account was logged in before before, a cookie file was created
        2. there is no such cookie file
        '''
        self.session = requests.Session()

    def is_login(self):
        ''' Login or not, two cases to consider:
        1. this account was logged in before before, a cookie file was created;
        2. there is no such cookie file  .
        return: boolean
        '''
        if not os.path.exists("conf.d/cookie.dat"):
            return False

        with open('conf.d/cookie.dat', 'rb') as f:
            cookies = pickle.load(f)
            cj = requests.cookies.RequestsCookieJar()
            cj._cookies = cookies
            self.session.cookies = cj

        r_get = self.session.get('http://www.douban.com')
        return 'UPLOAD_AUTH_TOKEN' in BeautifulSoup(r_get.text, 'lxml')

    def get_account(self):
        return json.load(open('/usr/local/info/douban.json', 'r'))

    def save_cookies_login(self):
        ''' Log in account and localize cookies for further explorations.
        '''
        if self.is_login():
            print("🕷 Cookies remain valid, already logged in.")
            return

        dhost = "http://accounts.douban.com/login"
        r_get = self.session.get(dhost)
        bs_get = BeautifulSoup(r_get.text, 'lxml')

        captcha_solution = self.rec_captcha(
            bs_get.find("img", {"id": "captcha_image"}))
        cid = bs_get.find("input", {"name": "captcha-id"})
        captcha_id = cid['value'] if cid else None
        account = self.get_account()

        params = {
            'form_email': account['email'],
            'form_password': account['password'],
            'captcha-solution': captcha_solution,
            'captcha-id': captcha_id}

        print(params)
        r_post = self.session.post(dhost, data=params)

        print(r_post.text)
        if "UPLOAD_AUTH_TOKEN" in r_post.text:
            print("Login SUCCEED.")
            # save cookies to local
            with open('conf.d/cookies.dat', 'wb') as f:
                pickle.dump(self.session.cookies._cookies, f)
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


Douban().save_cookies_login()


#         'captcha-id': captcha_id
#     }

#     session = requests.Session()
#     s = session.post(
#         "https://accounts.douban.com/login",
#         data=params)
#     response_obj = BeautifulSoup(s.text, features="lxml")
#     if 'UPLOAD_AUTH_TOKEN' in response_obj.text:
#         print("Login SUCCESS!")

#     # print(response_obj.text)

#     # status = open('captcha.jpg', 'r').read()
#     files = {'file': open('captcha.jpg', 'rb')}
#     params = {
#     r = session.post("https://www.douban.com", data=params, files=files)
#         'ck': "vapU",
#         'comment': "Status with image."
#     }

#     r = session.post("https://www.douban.com", data=params)
#     # response_obj = BeautifulSoup(r.text, features="lxml")
#     # print(response_obj.text)
#     # if response_obj.find("div", {"class": "messages"}) is not None:
#     # print(response_obj.find("div", {"class": "messages"}).get_text())
# else:
#     print("The CAPTCHA wasn't read correctly")
