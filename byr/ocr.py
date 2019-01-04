# -*- coding: utf-8 -*-

from PIL import Image
import os
import pytesseract
import enchant
import string
import re 

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# pre config image, remove background

class BYROCR:
	''' specifically designed for semi-auto captcha recognizing of bt.byr.cn
	'''
	def __init__(self):
		pass

	def pre_concert(self, f):
		img = Image.open(f)
		width, height = img.size
		threshold = 30
		for j in range(15, height-15):
			for i in range(20, width-20):
				p = img.getpixel((i, j))
				r, g, b = p
				if r > threshold or g > threshold or b > threshold:
					# img.putpixel((i, j), WHITE)
					print(' ', end="")
				else:
					# img.putpixel((i, j), BLACK)
					print('▓', end="")
					# print('🀫', end="")					
			print()
		return


if __name__ == '__main__':
	import urllib
	from urllib.request import urlretrieve

	with open ('login.php', 'rb') as f:
		for line in f:
			line = line.decode('utf-8')
			searchlink = re.search(r'(image\.php.*)\" border', line)
			if searchlink:
				urlretrieve('https://bt.byr.cn/' + searchlink.group(1).replace("amp;", ''), 'c.png')


	BYROCR().pre_concert('c.png')
