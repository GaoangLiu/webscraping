#!/user/bin/python3
from readfree import Readfree
import pprint
import datetime

# Time printing for debugging purpose 
# To see when the program went wrong.
print(datetime.datetime.now())
pprint.pprint(Readfree().get_account_info())




