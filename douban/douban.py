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
        pass 

    def is_login(self):
        ''' Login or not, two cases to consider:
        1. this account was logged in before before, a cookie file was created;
        2. there is no such cookie file  .
        return: boolean
        '''
        if not os.path.exists("conf.d/cookie.dat"):
            return False

        session = requests.Session()
        with open('conf.d/cookie.dat', 'rb') as f:
            cookies = pickle.load(f)
            cj = requests.cookies.RequestsCookieJar()
            cj._cookies = cookies
            session.cookies = cj

        r_get = session.get('http://www.douban.com')
        soup = BeautifulSoup(r_get.text, 'lxml')
        return 'UPLOAD_AUTH_TOKEN' in soup.text

    def get_account(self):
        return json.load(open('/usr/local/info/douban.json', 'r'))

    def save_cookies_login(self):
        ''' Log in account and localize cookies for further explorations.
        '''
        if self.is_login():
            print("🕷  Cookie remains valid, already logged in.")
            return
        else:
            print("🕷  Cookie is no more valid.")

        dhost = "http://www.douban.com/login"
        r_get = requests.get(dhost)
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

        session = requests.Session()
        s = session.post("https://accounts.douban.com/login",data=params)
        soup = BeautifulSoup(s.text, features="lxml")
        # print(soup.text)

        if 'UPLOAD_AUTH_TOKEN' in soup.text:
            print("Login SUCCESS!")
            # save cookies to local
            with open('conf.d/cookie.dat', 'wb') as f:
                pickle.dump(session.cookies._cookies, f)
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
# print(Douban().is_login())



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
