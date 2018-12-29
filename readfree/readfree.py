import os
import requests
from urllib.request import urlretrieve, urlopen
from bs4 import BeautifulSoup
import pickle
import json


class Readfree:
	def __init__(self, account_json='/user/local/info/readfree.json'):
		self.account_json = account_json

	def is_login(self):
		# return either False or a session with cookie loaded 
		cookie_path = 'conf.d/cookies.dat'
		if not os.path.exists(cookie_path):
			return False 

		session = requests.Session()
		with open(cookie_path, 'rb') as f:
			cookies = pickle.load(f)
			cj = requests.cookies.RequestsCookieJar()
			cj._cookies = cookies
			session.cookies = cj

		r_get = session.get("http://readfree.me/accounts/profile/bluesea/wish/")
		if '/accounts/profile' in r_get.text:
			print("🕷  Yes, cookie remains valid.")
			return session
		else:
			return False

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

	def save_cookie_login(self):
		''' Log in account and localize cookies for further explorations. 
		return logged session 
		'''
		session = self.is_login()
		if session: return session

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
		return session


	def get_account_info(self):
		import re
		session = self.save_cookie_login()
		soup = BeautifulSoup(session.get('http://readfree.me').text, 'lxml')
		# print(soup)
		link = soup.find("a", href=re.compile(".*accounts/profile.*"))
		username = ''
		if link:
			username = re.search(r'profile/(.*)/wish', str(link)).group(1)
			print("username:", username)
			moresoup = BeautifulSoup(session.get("http://readfree.me" + link.attrs['href']).text, 'lxml')
			for item in moresoup.findAll('p', {"class":"muted"}):
				print(item.text)




	def parse_page_books(self):
		'''parse all the books on current pabe'''
		response = self.login()
		for book in response.findAll("a", {"class":"pjax"}):
			print(book)
			# print(book.text, book.attrs['href'])


if __name__ == '__main__':
	rf = Readfree('/usr/local/info/readfree.json')
	rf.save_cookie_login()










# image_file = Image.open("images/captcha.jpg") # open colour image
# image_file = image_file.convert('1') # convert image to black and white
# image_file.save('result.jpg')
# img = Image.open("result.jpg")
# OCR().remove_noise(img,1)
# print(OCR().image_to_string(img))

# Readfree().recognize_captcha('images/result.jpg')
