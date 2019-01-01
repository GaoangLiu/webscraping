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
        self.session = self.save_cookies_login()
        self.mainpage = "https://www.douban.com"

    def is_login(self):
        ''' Login or not, two cases to consider:
        1. this account was logged in before before, a cookie file was created;
        2. there is no such cookie file  .
        return False if there is no cookie or cookie is no more valid,
        otherwise return the session
        '''
        if not os.path.exists("/usr/local/info/dbcookie.dat"):
            return False

        session = requests.Session()
        with open('/usr/local/info/dbcookie.dat', 'rb') as f:
            cookies = pickle.load(f)
            cj = requests.cookies.RequestsCookieJar()
            cj._cookies = cookies
            session.cookies = cj
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
            session.headers = headers

        r_get = session.get('http://www.douban.com')
        soup = BeautifulSoup(r_get.text, 'lxml')
        return session if 'UPLOAD_AUTH_TOKEN' in soup.text else False

    def get_account(self):
        return json.load(open('/usr/local/info/douban.json', 'r'))

    def save_cookies_login(self):
        ''' Log in account and localize cookies for further explorations.
        '''
        session = self.is_login()
        if session:
            print("🕷  Cookie remains valid, already logged in.")
            return session
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
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
        session.headers = headers

        s = session.post("https://accounts.douban.com/login", data=params)
        soup = BeautifulSoup(s.text, features="lxml")
        # print(soup.text)

        if 'UPLOAD_AUTH_TOKEN' in soup.text:
            print("Login SUCCESS!")
            # save cookies to local
            with open('/usr/local/info/dbcookie.dat', 'wb') as f:
                pickle.dump(session.cookies._cookies, f)
        return session

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
        ck_value = self.session.cookies['ck']
        # files = {'media': open('images/captcha.jpg', 'rb').read()}
        # img=open('images/captcha.jpg', 'rb').read()
        self.session.post(self.mainpage, data={'ck':ck_value, 'comment': content})
        print("🐜 status posted SUCCEED !")


if __name__ == '__main__':
    db = Douban()
    db.post_status("-- sent with Python.")


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
