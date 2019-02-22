#!/user/bin/python3
from rfv2 import ReadFree
import pprint
import arrow
import sys
import time 

# Time printing for debugging purpose 
# To see when the program went wrong.
# choice = sys.argv[1]

while True:
	try:
		rf = ReadFree('/usr/local/info/ssruoz_rf.dat', '/usr/local/info/ssruoz_rf.json')    	
		print(arrow.now().format('YYYY-MM-DD HH-mm'))
		pprint.pprint(rf.getAccountInfo())
	except Exception as e:
		print(e)
	time.sleep(3600)




