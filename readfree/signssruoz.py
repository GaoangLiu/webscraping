#!/user/bin/python3
from rfv2 import ReadFree
import pprint
import arrow
import sys 

# Time printing for debugging purpose 
# To see when the program went wrong.
choice = sys.argv[1]

while True:
	rf = ''
	if int(choice) == 1:
		rf = ReadFree('/usr/local/info/rfcookies.pkl', '/usr/local/info/readfree.json')
	else:
		rf = ReadFree('/usr/local/info/ssruoz_rf.dat', '/usr/local/info/ssruoz_rf.json')    

	print(arrow.now().format('YYYY-MM-DD HH-mm'))
	pprint.pprint(rf.getAccountInfo())
	break
	time.sleep(3)




