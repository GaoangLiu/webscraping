import pickle
import time
import sys
import os
import re
import requests
import random
import subprocess
import getpass 
import shutil
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from PIL import Image

# Specify your own path to store and load cookies
COOKIE_FILE = "byrcookies.pkl"
MAIN_PAGE = 'https://bt.byr.cn/'
LOGIN_PAGE = 'https://bt.byr.cn/login.php'
SESSION = requests.Session()
ACCOUNT = {}

def get_account():
	''' user id
	:rtype: int
	'''
	soup = BeautifulSoup(SESSION.get(MAIN_PAGE).text, 'lxml')
	# soup = BeautifulSoup(open('fayder.html', 'rb').read(), 'lxml')
	medium = soup.find('span', {'class': 'medium'})

	user = medium.find('a', href=re.compile(r'userdetails\.php'))    
	ACCOUNT['userid'] = int(user.attrs['href'].split("=")[-1])
	ACCOUNT['username'] = user.text

	quotas = [
		item for item in medium.text.split() if re.search(
			r'(\d+)', item)]

	for i, e in enumerate(['bonus', 'invite', 'upload_rank',
						   'ratio', 'uploaded', 'downloaded', 'seeding', 'leeching']):
		ACCOUNT[e] = quotas[i]

	units = re.findall(r'([GMT]B)', medium.text)		
	ACCOUNT['uploaded'] += ' ' + units[0] + ' ⬆'
	ACCOUNT['downloaded'] += ' ' + units[1] + ' ⬇'

	return ACCOUNT

def print_account():
	''' print account info for debugging purpose
	itype: dict / rtype: None
	'''
	for k, v in ACCOUNT.items():
		print(' {:<13} : {:<20}'.format(k, v))


def login_with_cookie():
	if not os.path.exists(COOKIE_FILE):
		return [False, None]

	SESSION.headers = {'User-Agent': 'Mozilla/5.0'}
	with open(COOKIE_FILE, 'rb') as f:
		SESSION.cookies.update(pickle.load(f))

	resp = SESSION.get(MAIN_PAGE)
	uname = ''
	if resp.url == MAIN_PAGE:
		get_account()
		print(
			">> Cookies remain valid, welcome back, " +
			ACCOUNT['username'] +
			"! 🐜 ")
		print_account()
		return [SESSION, resp]
	return [False, None]


def preview(image_file):
	img = Image.open(image_file)
	width, height = img.size
	threshold = 30

	for j in range(15, height - 15):
		for i in range(20, width - 20):
			p = img.getpixel((i, j))
			r, g, b = p
			if r > threshold or g > threshold or b > threshold:
				print(' ', end="")
			else:
				print('▓', end="")
		print()


def login():
	# First, login with cookies
	SESSION, resp = login_with_cookie()
	if SESSION:
		return [SESSION, resp]
	SESSION = requests.Session()
	SESSION.headers = {'User-Agent': 'Mozilla/5.0'}
	# html = open("login.html", 'rb').read()
	soup = BeautifulSoup(SESSION.get(LOGIN_PAGE).text, 'lxml')
	captcha_link = MAIN_PAGE + soup.findAll('img')[0].attrs['src']
	print(
		">> open the following link for checking captcha:",
		captcha_link,
		sep="\n")
	urlretrieve(captcha_link, 'captcha.jpg')
	preview('captcha.jpg')

	imagehash = captcha_link.split("=")[-1]
	imagestring = input(">> type in here the captcha value: ")
	username = input(">> byr username: ")
	password = getpass.getpass('>> byr password: ')

	params = {
		'username': username,
		'password': password,
		"imagestring": imagestring,
		'imagehash': imagehash,
	}
	# print(params)

	resp = SESSION.post('https://bt.byr.cn/takelogin.php', data=params)
	with open(COOKIE_FILE, 'wb') as f:
		print(">> login SUCCEED. saving cookies...")
		pickle.dump(SESSION.cookies, f)
	return (SESSION, resp)

# --------------------------------------------------------------------
SESSION, resp = login()
# --------------------------------------------------------------------

def retrieve_torrent():
	soup = BeautifulSoup(resp.text, 'lxml')
	torrents = []
	for link in soup.findAll('a', href=re.compile("^download*")):
		down = MAIN_PAGE + link.attrs['href']
		torrent_name = down.split("=")[-1] + ".torrent"
		print('>> Downloading torrent', down, '>', torrent_name)

		r = SESSION.get(down, allow_redirects=True)
		open(torrent_name, 'wb').write(r.content)
		torrents.append(torrent_name)
	return torrents

def parse_torrent(t):
	# given a torrent, return its size in unit and a random port
	cmd = 'transmission-show ' + t + " | grep Total"
	size, unit = subprocess.check_output(cmd, shell=True).split()[2:4]
	size, unit = float(size), unit.decode('utf-8')
	port = random.randint(20000, 30000)
	return(size, unit, port)


def routine():
	global resp
	resp = SESSION.get(MAIN_PAGE)
	torrents = retrieve_torrent()
	_, _, free = [ u // (2**30) for u in shutil.disk_usage('/')]
	for t in torrents:
		if os.path.exists(t): continue
		size, unit, port = parse_torrent(t)
		if unit == 'MB' and free >= 1 or free >= size:
			free -= 1 if unit == 'MB' else size 
			os.system("transmission-cli -p " + str(port) + ' ' + t + ' &>/dev/null &')


def download_files():
	print(">> Terminating transmission-cli & Cleaning Downloads, torrents resume...")
	os.system("pkill -f transmission")  # terminal previous threads
	os.system("sleep 10; rm -rf /root/Downloads/*")
	os.system("rm -f /root/.config/transmission/torrents/*")  # removing torrents
	os.system("rm -f /root/.config/transmission/resume/*")    # removing resumes 	
	os.system("rm -f *.torrent")    # removing resumes 		

	_, _, free = [ u // (2**30) for u in shutil.disk_usage('/')]
	print(">> Available memory: " + str(free) + ' GB')

	# to clear redundant seeds
	SESSION.get("https://bt.byr.cn/takeflush.php?id=" + str(ACCOUNT['userid']))
	sleep_period = 30
	print(">> Seeds was flushed. Sleep for {:<2} seconds".format(sleep_period))
	time.sleep(sleep_period)

	for t in retrieve_torrent():
		try:
			size, unit, port = parse_torrent(t)
			if unit == 'MB' or unit == 'GB' and size < free:
				free -= 1 if unit == 'MB' else size
				print(">> Downloading " + t)
				os.system("transmission-cli -p " + str(port) + " " + t + " &>/dev/null&")
		except Exception as e:
			print(e)
			continue


cter = 1000
while True:
	sleep_period = 1800 
	try:
		if cter >= 24 * 3600 // sleep_period:
			cter = 0 
			download_files()
		routine()
		cter += 1
		time.sleep(sleep_period)
	except Exception as e:
		print("WHILE TRUE exception : ")
		print(e)
