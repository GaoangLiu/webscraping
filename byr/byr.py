import pickle
import time
import sys
import os
import re
import requests
import random
import subprocess
import getpass 
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
			r'(\d)+', item)]

	for i, e in enumerate(['bonus', 'invite', 'upload_rank',
						   'ratio', 'uploaded', 'downloaded', 'seeding', 'leeching']):
		ACCOUNT[e] = quotas[i]
	ACCOUNT['uploaded'] += ' GB ⬆'
	ACCOUNT['downloaded'] += ' GB ⬇'

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


def download_files():
	print(">> Terminating transmission-cli process and clean ~/Downloads/ + ../torrents/...")
	os.system("pkill -f transmission")  # terminal previous threads
	os.system("sleep 10; rm -rf /root/Downloads/*")
	os.system("rm -f /root/.config/transmission/torrents/*")  # removing torrents

	AVAIL_DEV = subprocess.check_output('df -h | grep "/dev/vda"', shell=True).split()[3].decode("utf-8")
	memory = float(re.sub(r'[GM]', '', AVAIL_DEV))
	print(">> Available memory: " + AVAIL_DEV)

	# to clear redundant seeds
	SESSION.get("https://bt.byr.cn/takeflush.php?id=" + str(ACCOUNT['userid']))
	print(">> Seeds was flushed. Sleep for 10 minutes. ")
	time.sleep(500)

	for t in retrieve_torrent():
		try:
			cmd = 'transmission-show ' + t + " | grep Total"
			filesize, units = subprocess.check_output(
				cmd, shell=True).split()[2:4]
			filesize, units = float(filesize), units.decode('utf-8')
			print(t, filesize, units)

			port = random.randint(20000, 30000)
			cmd = "transmission-cli -p " + str(port) + " " + t + " &>/dev/null&"
			if units == 'MB' or units == 'GB' and filesize < memory:
				memory -= 1 if units == 'MB' else filesize
				print(">> Downloading " + t)
				os.system(cmd)
		except Exception as e:
			print(e)
			continue


while True:
	try:
		download_files()
		time.sleep(3600 * 12)
	except Exception as e:
		print("WHILE TRUE exception : ")
		print(e)
