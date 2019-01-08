from hupu import Hupu, MAINPAGE, SPURS
import time, random, re, os, sys, datetime

hp = Hupu()
hp.login()

while True:
	try:
		print(datetime.datetime.now(), 'Normal')				
		hp.driver.get('https://my.hupu.com/Elena_Greco')
		if random.randint(1, 100) == 21:
			hp.water_bbs()
		time.sleep(60)
	except Exception as e:
		print(e)
		print(">> sleep for 1800 seconds now ...")
		time.sleep(1800)
		hp.login()
		print(">> hupu re-logged in.")		


