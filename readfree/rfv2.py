import os
import requests
from urllib.request import urlretrieve, urlopen
from bs4 import BeautifulSoup
import pickle
import json
import re
from pprint import pprint
import arrow

COOKIE_FILE = '/usr/local/info/rfcookies.pkl'
ACCOUNT = '/usr/local/info/readfree.json'

class ReadFree():
    def __init__(self):
        self.mainpage = "http://readfree.me"
        self.loginpage = "https://readfree.me/auth/login/?next=/"
        self.session = requests.Session()
        self.session.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Inter Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
            "Accppt": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*,q=0.8"}

    def recognizeCaptcha(self, soup):
        captcha = soup.find("img", {"class": "captcha"})
        if captcha:
            image_path = "images/captcha.jpg"
            urlretrieve(self.mainpage + captcha['src'], image_path)
            os.system("open images/captcha.jpg")
            return input(">> Type in what u see: ").strip()

    def manulLogin(self):
        account = json.load(open(ACCOUNT, 'r'))
        soup = BeautifulSoup(self.session.get(self.loginpage).text, 'lxml')
        csrftoken = soup.find("input", {"name":"csrfmiddlewaretoken"})['value']
        print('csrftoken', csrftoken)

        captcha_0 = soup.find("input", {"name": "captcha_0"})["value"]
        captcha_1 = self.recognizeCaptcha(soup)

        params = {
            'login': account['email'],
            'password': account['password'],
            'csrfmiddlewaretoken': csrftoken,
            'captcha_0': captcha_0,
            'captcha_1': captcha_1}
        r_post = self.session.post(self.loginpage, data=params)

        if '/accounts/settings/' in r_post.text:
            print("MANUAL LOGIN SUCCEED.")
            pickle.dump(self.session.cookies, open(COOKIE_FILE, 'wb'))

    def login(self):
        if os.path.exists(COOKIE_FILE):
            self.session.cookies.update(pickle.load(open(COOKIE_FILE, 'rb')))
            info = 'LOGIN SUCCEED with COOKIES' if '/accounts/settings' in self.session.get(self.mainpage).text else 'LOGIN FAILED'
            print(info)
            return 
        self.manulLogin()

    def getAccountInfo(self):
        self.login()
        soup = BeautifulSoup(self.session.get(self.mainpage).text, 'lxml')
        link = soup.find("a", href=re.compile(".*accounts/profile.*"))
        infos = []
        if link:
            infos.append(re.search(r'profile/(.*)/wish', str(link)).group(1))
            moresoup = BeautifulSoup(self.session.get(self.mainpage + link.attrs['href']).text, 'lxml')
            for item in moresoup.findAll('p', {"class": "muted"}):
                infos.append(item.text)

        return infos


if __name__ == '__main__':
    rf = ReadFree()
    print(arrow.now().format('YYYY-MM-DD HH-mm'))
    pprint(rf.getAccountInfo())






