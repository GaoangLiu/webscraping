import pickle
import requests
from urllib.request import urlretrieve

with open('conf.d/cookies.dat', 'rb') as f:
    cookies = pickle.load(f)
cj = requests.cookies.RequestsCookieJar()
cj._cookies = cookies
session = requests.Session()
session.cookies = cj

# r_get = session.get("http://readfree.me/rank/365/")
# print(r_get.text)

href = "/edition/04e031e4f8e49f7b285a0ffa4be01288/down/Rust%E6%89%8B%E5%86%8C.pdf"
d_link = "http://readfree.me" + href
with open('warechris.pdf', 'wb') as f:
    f.write(session.get(d_link).content)
