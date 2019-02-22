#!/user/bin/python3
from rfv2 import ReadFree
import pprint
import arrow
import sys 
import random
import time

while True:
	try:
		rf = ReadFree('/usr/local/info/rfcookies.pkl', '/usr/local/info/readfree.json')
		rf.login()
		rf.shuffleUploadBooks()
	except Exception as e:
		print(e)
	time.sleep(random.randint(3600, 7200))