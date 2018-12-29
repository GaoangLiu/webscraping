import pickle, requests

with open('conf.d/cookies.dat', 'rb') as f:
	cookies = pickle.load(f)
cj = requests.cookies.RequestsCookieJar() 
cj._cookies = cookies
session = requests.Session()
session.cookies = cj

r3 = session.get("http://readfree.me/rank/365/")
print(r3.text)