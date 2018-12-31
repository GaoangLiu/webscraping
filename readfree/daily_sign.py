#!/user/bin/python3
from readfree import Readfree
import time
import pprint

rf = Readfree()

def keep_sign_in():
    # Check account info every few hours, just to keep logged in and
    # thus more credits returned
    while True:
        pprint.pprint(rf.get_account_info())
        time.sleep(7200)

keep_sign_in()

