from hupu import Hupu, MAINPAGE, SPURS
import time, random, re, os, sys, datetime

# hp = Hupu()
# hp.login()
# is_logout = False

hp = Hupu()
while True:
	try:
		hp = Hupu()
		hp.login()
		print(datetime.datetime.now(), 'Normal')				
		hp.driver.get('https://my.hupu.com/')
		hp.water_bbs()
		time.sleep(3)
		hp.driver.quit()
		time.sleep(random.randint(300, 600))
	except Exception as e:
		print(e)
		print(datetime.datetime.now(), 'Exception')		
		hp.driver.quit()
		time.sleep(300)


