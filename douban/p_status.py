#!/user/bin/python3
from douban import *

db = Douban()
db.post_status(sys.argv[1])