import pickle
import time
import sys
import os
import re
import requests
import random
import subprocess
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from PIL import Image

# Specify your own path to store and load cookies
COOKIE_FILE = "byrcookies.pkl"
MAIN_PAGE = 'https://bt.byr.cn/'
LOGIN_PAGE = 'https://bt.byr.cn/login.php'

def login_with_cookie():
	if not os.path.exists(COOKIE_FILE):
		return [False, None] 

	session = requests.Session()
	session.headers={'User-Agent': 'Mozilla/5.0'}

	with open(COOKIE_FILE, 'rb') as f:
		session.cookies.update(pickle.load(f))

	resp = session.get(MAIN_PAGE)
	if resp.url == MAIN_PAGE:
		print(">> cookies remain valid.")
		return [session, resp]
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
	session, resp = login_with_cookie()
	if session:
		return [session, resp]

	session = requests.Session()
	session.headers={'User-Agent': 'Mozilla/5.0'}
	# html = open("login.html", 'rb').read()
	soup = BeautifulSoup(session.get(LOGIN_PAGE).text, 'lxml')
	captcha_link = MAIN_PAGE + soup.findAll('img')[0].attrs['src']
	print(">> open the following link for checking captcha:", captcha_link, sep="\n")
	urlretrieve(captcha_link, 'captcha.jpg')
	preview('captcha.jpg')

	imagehash = captcha_link.split("=")[-1]
	imagestring = input(">> type in here the captcha value: ")
	username = input(">> byr username: ")
	password = input(">> byr password: ")

	params = {
		'username': username,
		'password': password,
		"imagestring": imagestring,         
		'imagehash': imagehash,
		}
	print(params)

	resp = session.post('https://bt.byr.cn/takelogin.php', data=params)
	with open (COOKIE_FILE, 'wb') as f:
		print(">> login SUCCEED. saving cookies...")
		pickle.dump(session.cookies, f)
	return (session, resp)




def retrieve_torrent():
	session, resp = login()
	soup = BeautifulSoup(resp.text, 'lxml')   
	torrents = []
	for link in soup.findAll('a', href=re.compile("^download*")) :
		down = MAIN_PAGE + link.attrs['href']
		torrent_name = down.split("=")[-1] + ".torrent"
		print(down, torrent_name)

		r = session.get(down, allow_redirects=True)
		open(torrent_name, 'wb').write(r.content)
		torrents.append(torrent_name)
	return torrents


def download_files():
	AVAIL_DEV = subprocess.check_output('df -h | grep "/dev/vda"', shell=True).split()[3].decode("utf-8")     
	memory = float(re.sub(r'[GM]', '', AVAIL_DEV))
	os.system("rm -rf /root/Downloads/*")
	os.system("pkill -f transmission") # terminal previous threads 

	for t in retrieve_torrent():
		try:
			cmd = 'transmission-show ' + t + " | grep Total"
			filesize, units = subprocess.check_output(cmd, shell=True).split()[2:4]
			filesize, units = float(filesize), units.decode('utf-8')
			print(t, filesize, units)

			port = random.randint(20000, 30000)            
			cmd = "transmission-cli -p " + str(port) + " " + t + "&>/dev/null&"
			if units == 'MB' or units == 'GB' and filesize < memory:
				memory -= 1 if units == 'MB' else filesize
				print(">> downloading " + t)
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


