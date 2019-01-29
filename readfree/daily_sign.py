#!/user/bin/python3
from rfv2 import ReadFree
import pprint
import datetime

# Time printing for debugging purpose 
# To see when the program went wrong.
print(datetime.datetime.now())
pprint.pprint(ReadFree().getAccountInfo())




