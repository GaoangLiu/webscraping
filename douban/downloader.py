import os
import requests
import subprocess
import sys
import pickle
import json
import time
from urllib.request import urlretrieve, urlopen
from bs4 import BeautifulSoup
from PIL import Image
from PIL import ImageOps
from ocr import OCR


IMAGE_PATH = "/Users/alpha/Downloads/dbimage/"



s = requests.Session()
s.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
s.cookies.update(pickle.load(open('/usr/local/info/dbcookie.dat', 'rb')))


def get_status_image(source):
	print(">> visiting page", source)
	html = s.get(source)
	soup = BeautifulSoup(html.text, 'lxml')

	visited = {'u86594717-8.jpg':True}
	for e in soup.findAll('img'):
		src = e.attrs['src']
		if 'small' in src or 'status' not in src: continue
		imgid = src.split('/')[-1]
		if imgid in visited: continue
		print('>> retrieving', imgid)
		visited[imgid] = True
		urlretrieve(src, IMAGE_PATH+imgid)

source = 'https://www.douban.com/people/86594717/statuses'
source = 'https://www.douban.com/people/kusoing/statuses'
for p in range(81, 100):
	next_s = source+'?p='+str(p)
	get_status_image(next_s)
	time.sleep(3)

