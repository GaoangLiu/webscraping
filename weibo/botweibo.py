from selenium import webdriver
import time, sys, os, re, random
import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from selenium.webdriver.chrome.options import Options
import logging 
import json
import pickle 
from weibo import Weibo

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TODAYSHOT = 'http://www.pniao.com/Mov/todayClick'
TUIJIAN_PAGE = 'http://www.pniao.com/Mov/recommd/Pn1.html'
MAINPAGE = 'http://www.pniao.com/'
COOKIE_FILE = '/usr/local/info/pniaoboy.pkl'

class Pniao():
	def __init__(self):
		options = Options()
		options.add_argument('--headless')
		options.add_argument('--disable-gpu')
		options.add_argument('--no-sandbox')
		options.add_argument('--disable-dev-shm-usage')		
		self.driver = webdriver.Chrome(options=options)
		self.driver.set_window_size(1440, 900)

		# To force re-login every few hours  
		if random.randint(0, 20) == 10:
			os.remove(COOKIE_FILE)

		if not os.path.exists(COOKIE_FILE):
			self.updateCookies()

		self.driver.get(MAINPAGE)        
		cookies = pickle.load(open(COOKIE_FILE, "rb"))
		for cookie in cookies:
			self.driver.add_cookie(cookie)
		# self.driver.set_page_load_timeout(30)
		self.cover = 'poster.jpg'

	def updateCookies(self):
		self.driver.get(MAINPAGE)
		self.driver.find_element_by_class_name('userName').click()
		self.driver.find_element_by_xpath('//input[@name="login_userName"]').send_keys('pniaoboy')
		self.driver.find_element_by_xpath('//input[@name="login_userPsw"]').send_keys('pniaoboy999')        
		self.driver.find_element_by_class_name('submit').click()
		logger.info("LOGIN SUCCEED !")

		time.sleep(3)        
		pickle.dump(self.driver.get_cookies(), open(COOKIE_FILE, "wb"))        


	def get_bangdan(self):
		''': webdrive object
		'''
		choice = 'http://www.pniao.com/Mov' + random.choice(['', '/weekup', '/movie', '/tv', '/doc', '/comic', '/weekclick'])
		if choice == 'http://www.pniao.com/Mov/weekclick':
			choice += '/pn' + str(random.randint(1, 5)) + '.html'
		self.driver.get(choice)
		soup = BeautifulSoup(self.driver.page_source, 'lxml')       
		bangdan = []
		for links in soup.findAll('h4'):
			bangdan.append([links.a.attrs['href'], links.text])
		logger.debug(bangdan)
		return bangdan


	def getDoubanCover(self, movie_url):
		s = requests.Session()
		soup = BeautifulSoup(s.get(movie_url + '/photos?type=R').text, 'lxml')
		first_cover = soup.find('div', {'class':'cover'})
		if not first_cover: return False # no cover image was found
		# print(first_cover.a)
		coverurl = first_cover.a.img.attrs['src'].replace('/m/', '/l/')
		urlretrieve(coverurl, 'poster.webp')        
		return True


	def parse_film_info(self, url):
		self.driver.get(url)
		time.sleep(2)       
		source = self.driver.page_source
		soup = BeautifulSoup(source, 'lxml')
		# logger.info(soup)
		try:
			poster = soup.find('img', {'data-url': re.compile(r'.*\.jpg')}).attrs['data-url']			
			urlretrieve(poster, 'poster.jpg')
		except Exception as e:
			print('urlretrieve falled', e)

		# overwrite poster.jpg if there is one
		douban_url = soup.find('a', {'href': re.compile(r'https://movie.douban.com/subject/\d+')}).attrs['href']        
		if self.getDoubanCover(douban_url): self.cover = 'poster.webp'

		status = ""
		fullname = soup.findAll('h1')[-1].text
		status += fullname
		logger.debug(fullname)
		has_sources = False 

		for e in soup.findAll('div', {'class': 'downUrlList'}):
			# print(e.a, e.text)            
			pan = re.findall(r'(https://pan.baidu.com/.*?)\"', str(e.a))
			if pan:
				has_sources = True
				status += "\n度盘：" + pan[0]

			pancode = re.findall(r'(?:提取码|密码)(?::)*\s*(\w{4})', str(e.text))                
			if pancode:
				status += '\n密码：' + pancode[0]
				# print(pancode)

			magnet = re.findall(r'(magnet:.*?)\"', str(e.a).replace('&amp;', '&'))
			for maglink in magnet:
				if len(status + maglink) > 135: continue
				has_sources = True                
				status += '\n磁链：' + maglink
				# print(status)

		return status if has_sources else None

	def pick_a_film(self, bangdan):
		try:
			posted = json.load(open('film.json', 'r'))
		except Exception as e:
			posted = {}
			logger.warning('film.json loaded FAILED.')
			# raise e

		for url, name in bangdan:
			if url not in posted:
				posted[url] = 'posted'
				json.dump(posted, open('film.json', 'w'), indent=2)
				return self.parse_film_info(url)                

		logger.debug(bangdan)
		return self.parse_film_info(random.choice(bangdan)[0])

	def postSingleFilm(self, url=None):
		status = self.parse_film_info(url) if url else self.pick_a_film(self.get_bangdan()) 
		status += "\n#电影# #电视剧#"
		print(status) 
		if status:
			w = Weibo()
			w.login()
			w.postStatus(status, [self.cover])
			w.safeWaterFeeds()
			w.tearDown()

if __name__ == '__main__':
	url = None
	while True:
		try:
			pn = Pniao()
			pn.postSingleFilm(url)
			pn.driver.quit()
			time.sleep(random.randint(600, 1800))
		except Exception as e:
			print(e)
			time.sleep(600)            




