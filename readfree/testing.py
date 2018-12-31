import pickle
import requests
from urllib.request import urlretrieve
import sys
from readfree import Readfree
from pprint import pprint


rf = Readfree()
rf.parse_single_book("hosi≠")
# rf.parse_hot_books()
sys.exit(0)


pprint(rf.get_account_info())
session = rf.save_cookie_login()

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Inter Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
    "Accppt": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*,q=0.8"}


href = "/edition/04e031e4f8e49f7b285a0ffa4be01288/down/Rust%E6%89%8B%E5%86%8C.pdf"
href = "/edition/39792ffa3216e3873d26ebba79f157ab/down/%E5%A4%A7%E6%B1%9F%E5%A4%A7%E6%B2%B3%E5%9B%9B%E9%83%A8%E6%9B%B2%E8%AF%BB%E5%AE%A2%E6%96%87%E5%8C%96%E5%87%BA%E5%93%81%E6%AC%A2%E4%B9%90%E9%A2%82%E5%87%BA%E5%93%81%E6%96%B9%E6%AD%A3%E5%8D%88%E9%98%B3%E5%85%89%E6%96%B0%E5%89%A7%E5%A4%A7%E6%B1%9F%E5%A4%A7%E6%B2%B3%E5%8E%9F%E8%91%97%E5%B0%8F%E8%AF%B4%E7%8E%8B%E5%87%AF%E6%9D%A8%E7%83%81%E8%91%A3%E5%AD%90%E5%81%A5%E4%B8%BB%E6%BC%94%E8%B1%86%E7%93%A39.2%E9%AB%98%E5%88%86_-_%E9%98%BF%E8%80%90.azw3.pdf"
d_link = "http://readfree.me" + href
print("Downloading book ... ")
with open('djdh.pdf', 'wb') as f:
    f.write(session.get(d_link, headers=headers).content)


