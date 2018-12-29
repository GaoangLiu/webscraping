import pickle
import requests
from urllib.request import urlretrieve
import sys
from readfree import Readfree


Readfree().get_account_info()

def keep_sign_in():
	# just to get more credits 
	while True:
		Readfree().get_account_info()


sys.exit(0)
with open('conf.d/cookies.dat', 'rb') as f:
    cookies = pickle.load(f)
cj = requests.cookies.RequestsCookieJar()
cj._cookies = cookies
session = requests.Session()
session.cookies = cj

r_get = session.get("http://readfree.me/accounts/profile/bluesea/wish/")
print(r_get.text)
if '/accounts/profile' in r_get.text:
	print("🕷 Yes, cookies remain valid.")

href = "/edition/04e031e4f8e49f7b285a0ffa4be01288/down/Rust%E6%89%8B%E5%86%8C.pdf"
d_link = "http://readfree.me" + href
with open('warechris.pdf', 'wb') as f:
    f.write(session.get(d_link).content)
