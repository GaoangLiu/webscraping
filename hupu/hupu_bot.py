from hupu import Hupu, MAINPAGE, SPURS
import time, random, re, os, sys, datetime

hp = Hupu()
hp.login()

while True:
	try:
		print(datetime.datetime.now(), 'Normal')				
		hp.driver.get(SPURS)
		if random.randint(1, 20) > 18:
			hp.water_bbs()
		time.sleep(60)
	except Exception as e:
		print(e)


