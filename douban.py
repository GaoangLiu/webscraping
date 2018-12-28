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


class Account:
    def __init__(self):
        pass 

    def login(self):
        pass 

    def recognize_captcha(self):
        OCR().process()

Account().recognize_captcha()

# # html = urlopen("http://www.pythonscraping.com/humans-only")
# html = urlopen("http://www.douban.com/login")
# bsobj = BeautifulSoup(html, features='lxml')

# image_location = bsobj.find("img", {"id": "captcha_image"})["src"]
# urlretrieve(image_location, 'captcha.jpg')

# os.system("open captcha.jpg")
# captcha_solution = input("input what u see : ")

# captcha_id = bsobj.find("input", {"name": "captcha-id"})["value"]
# print("img_link  :", image_location)
# print("captcha_id:", captcha_id)


# if len(captcha_solution) > 0:
#     params = {
#         'form_email': 'windycat@pm.me',
#         'form_password': 'douban@2019',
#         'captcha-solution': captcha_solution,
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
