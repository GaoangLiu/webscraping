from hupu import Hupu, MAINPAGE, SPURS
import time, random, re, os, sys, datetime

hp = Hupu()
hp.login()
is_logout = False

while True:
	try:
		if is_logout: 
			hp = Hupu()
			hp.login()
		print(datetime.datetime.now(), 'Normal')				
		hp.driver.get('https://my.hupu.com/')
		hp.water_bbs()
		time.sleep(300)
	except Exception as e:
		print(e)
		print(datetime.datetime.now(), 'Exception')		
		hp.driver.quit()
		time.sleep(300)
		is_logout = True


