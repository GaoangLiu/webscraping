import os
import requests
from urllib.request import urlretrieve, urlopen
from bs4 import BeautifulSoup
import pickle
import json


class Readfree:
	def __init__(self, account_json):
		self.account_json = account_json

	def recognize_captcha(self, img):
		OCR().process(img)

	def getAccount(self, accountJson):
		return json.load(open(accountJson, 'r'))

	def recognizeCaptcha(self, bsobj):
		''' retrieve image from bsobj : beautiful soup object
		input: bs_obj
		output: string
		'''
		captcha = bsobj.find("img", {"class": "captcha"})
		text = ''
		if captcha:
			image_path = "images/captcha.jpg"
			urlretrieve('http://readfree.me' + captcha['src'], image_path)
			os.system("open images/captcha.jpg")
			text = input("==Type in what u see: ").strip()
			# self.recognize_captcha(image_path)
		return text

	def saveCookiesLogin(self):
		''' Log in account and localize cookies for further explorations. 
		'''
		dhost = "http://readfree.me/accounts/login/?next=/"
		session = requests.Session()
		r_get = session.get(dhost)
		account = self.getAccount(self.account_json)

		csrftoken = r_get.cookies['csrftoken']
		bsobj = BeautifulSoup(r_get.text, 'lxml')
		captcha_0 = bsobj.find("input", {"name": "captcha_0"})["value"]
		captcha_1 = self.recognizeCaptcha(bsobj)
		# print(captcha_0, captcha_1)

		params = {
			'email': account['email'],
			'password': account['password'],
			'csrfmiddlewaretoken': csrftoken,
			'captcha_0': captcha_0,
			'captcha_1':captcha_1}
		r_post = session.post(dhost, data=params)

		if "/accounts/logout/" in r_post.text:
			print("Login SUCCEED.")
			# save cookies to local
			with open ('conf.d/cookies.dat', 'wb') as f:
				pickle.dump(session.cookies._cookies, f)
		return 


	def parse_page_books(self):
		'''parse all the books on current pabe'''
		response = self.login()
		for book in response.findAll("a", {"class":"pjax"}):
			print(book)
			# print(book.text, book.attrs['href'])


rf = Readfree('/usr/local/info/readfree.json')
rf.saveCookiesLogin()










# image_file = Image.open("images/captcha.jpg") # open colour image
# image_file = image_file.convert('1') # convert image to black and white
# image_file.save('result.jpg')
# img = Image.open("result.jpg")
# OCR().remove_noise(img,1)
# print(OCR().image_to_string(img))

# Readfree().recognize_captcha('images/result.jpg')
