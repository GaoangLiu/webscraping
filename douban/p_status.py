#!/user/bin/python3
from douban import *
from dbwebdriver import *

def is_image(fname):
	return fname.endswith(tuple(['.jpg', '.png', 'jpeg', '.svg', '.gif']))

args = sys.argv[1:]
if len(args) == 1 and not is_image(args[0]):
	db = Douban()	
	db.post_status(args[0])
else:
	post_status(args)


