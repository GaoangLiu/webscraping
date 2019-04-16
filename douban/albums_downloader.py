import os
import requests
import subprocess
import sys
import pickle
import json
import time
from urllib.request import urlretrieve, urlopen
from bs4 import BeautifulSoup
import re 
import random


IMAGE_PATH = "/Users/alpha/Downloads/albums/"

s = requests.Session()
s.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
s.cookies.update(pickle.load(open('/usr/local/info/dbcookie.dat', 'rb')))


def getImageID(strlink):
	pid = re.findall(r'p(\d+)\.jpg', strlink)[0]
	return pid


def get_image(pid, cter = 10):
	cpid = pid
	while cter > 0:
		cter -= 1
		src = 'https://img1.doubanio.com/view/photo/l/public/p{}.jpg'.format(cpid)	
		print('Downloading {}'.format(cpid))
		urlretrieve(src, IMAGE_PATH + cpid + '.jpg')
	
		# Getting the next image id 
		html = s.get('https://www.douban.com/photos/photo/{}/#image'.format(cpid))
		soup = BeautifulSoup(html.text, 'lxml')
		nextimage = soup.findAll('span', style=re.compile(r'background.*'))[1]
		cpid = getImageID(nextimage.attrs['style'])
		# if random.randint(0, 100) > 99:
			# time.sleep(1)

pid = '2534308533'
get_image(pid, 4000)

