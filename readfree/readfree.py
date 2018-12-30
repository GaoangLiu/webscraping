import os
import requests
from urllib.request import urlretrieve, urlopen
from bs4 import BeautifulSoup
import pickle
import json
import re


class Readfree:
	def __init__(self, account_json='/user/local/info/readfree.json'):
		self.account_json = account_json
		self.mainpage = "http://readfree.me"
		self.headers = {
			"User-Agent": "Mozilla/5.0 (Macintosh; Inter Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
			"Accppt": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*,q=0.8"}

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

		r_get = session.get(
			"http://readfree.me/accounts/profile/bluesea/wish/",
			headers=self.headers)
		if '/accounts/profile' in r_get.text:
			print("🕷  -- cookie remains valid.")
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
		if session:
			return session

		dhost = "http://readfree.me/accounts/login/?next=/"
		session = requests.Session()
		r_get = session.get(dhost, headers=self.headers)
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
			'captcha_1': captcha_1}
		r_post = session.post(dhost, data=params, headers=self.headers)

		if "/accounts/logout/" in r_post.text:
			print("Login SUCCEED.")
			# save cookies to local
			with open('conf.d/cookies.dat', 'wb') as f:
				pickle.dump(session.cookies._cookies, f)
		return session

	def get_account_info(self):
		''' there are only few infos on each user
		return : username
		'''

		session = self.save_cookie_login()
		soup = BeautifulSoup(session.get('http://readfree.me').text, 'lxml')
		# print(soup)
		link = soup.find("a", href=re.compile(".*accounts/profile.*"))
		infos = []
		if link:
			infos.append(re.search(r'profile/(.*)/wish', str(link)).group(1))
			moresoup = BeautifulSoup(
				session.get(
					"http://readfree.me" +
					link.attrs['href']).text,
				'lxml')
			for item in moresoup.findAll('p', {"class": "muted"}):
				infos.append(item.text)

		return infos

	def parse_page_books(self):
		'''parse all the books on current pabe'''
		response = self.login()
		for book in response.findAll("a", {"class": "pjax"}):
			print(book)
			# print(book.text, book.attrs['href'])

	def delete_history(self, action, n=3):
		'''remvoe the most recent n book-ACTION(push, download, edit, comment) histories
		to delete all histories, set n to be a very large number, e.g., 9999
		action: push | down | edition | talk
		return: None
		'''
		username = self.get_account_info()[0]
		downpage = "http://readfree.me/accounts/profile/" + username + "/" + action
		session = self.save_cookie_login()
		soup = BeautifulSoup(
			session.get(
				downpage,
				headers=self.headers).text,
			'lxml')
		counter = 0

		# print(soup.text)
		regex = r"/" + re.escape(action) + r"/.*/delete"
		for item in soup.findAll('a', href=re.compile(regex)):
			regex = r"(/" + re.escape(action) + r"/.*/delete)"
			dellink = self.mainpage + re.search(regex, str(item)).group(1)
			print(dellink)

			if counter >= n:
				return
			session.get(dellink, headers=self.headers)
			counter += 1

		# Keep deleting rest n - counter histories
		if counter == 0:  # no more history
			return
		self.delete_history(action, n - counter)


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
