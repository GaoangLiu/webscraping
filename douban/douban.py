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
		html = urlopen("http://www.douban.com/login")
		bsobj = BeautifulSoup(html, 'lxml')


		# Sometimes, we don't need to recognize captcha
		captcha = bsobj.find("img", {"id": "captcha_image"})
		if captcha:
			image_path = "images/captcha.jpg"
			urlretrieve(captcha['src'], image_path)
			self.recognize_captcha(image_path)


	def recognize_captcha(self, img):
		OCR().process(img)

Account().login()


# os.system("open captcha.jpg")
# captcha_solution = input("input what u see : ")

# captcha_id = bsobj.find("input", {"name": "captcha-id"})["value"]
# print("img_link  :", image_location)
# print("captcha_id:", captcha_id)


# if len(captcha_solution) > 0:
#     params = {
#         'form_email': 'douban@gmail.com',
#         'form_password': 'doubanadmin',
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
