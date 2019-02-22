from __future__ import unicode_literals
import os
import requests
from urllib.request import urlretrieve, urlopen
from bs4 import BeautifulSoup
import pickle
import json
import re
from pprint import pprint
import arrow
import random

class ReadFree():
    def __init__(self, cookie, account):
        self.mainpage = "http://readfree.me"
        self.loginpage = "https://readfree.me/auth/login/?next=/"
        self.session = requests.Session()
        self.cookie = cookie
        self.account = account
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
        account = json.load(open(self.account, 'r'))
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
            pickle.dump(self.session.cookies, open(self.cookie, 'wb'))

    def login(self):
        if os.path.exists(self.cookie):
            self.session.cookies.update(pickle.load(open(self.cookie, 'rb')))
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

    def uploadBook(self, bookurl):
        soup = BeautifulSoup(self.session.get(bookurl).text, 'lxml')
        pushnums = []
        for i in soup.findAll('span', {'class':'push-num'}):
            n = random.randint(1024, 2048) if i.text == '1k+' else int(i.text)  
            pushnums.append(n)

        maxpushdown = 0
        # author = soup.find('a', {'class':'z-link-search'}).text.strip()     
        # title = soup.find('a', {'class':'link-search'}).text.strip()
        # title = (title + '_' + author).replace(' ', '')
        title = downlink = ''

        for j, i in enumerate(soup.findAll('a', {'class':'book-down'})):
            down_number = i.text.replace('下载', '').strip('\n')
            down_number = random.randint(1024, 2048) if down_number == '1k+' else int(down_number)
            if down_number + pushnums[j] > maxpushdown:
                title = i.attrs.get('title')
                downlink = i.attrs.get('href')                
                maxpushdown = down_number + pushnums[j]
        print(maxpushdown, title, downlink)

        postfix = downlink.split('.')[-1]
        if postfix == 'pdf': return 

        bookname = 'books/' + title + "." + postfix
        print("Downloading book {}".format(bookname))
        with open(bookname, 'wb') as f:
            f.write(self.session.get('https://readfree.me' + downlink).content)

        if postfix == 'mobi':
            os.system('ebook-convert {} {}'.format(bookname, 'books/' + title + ".epub"))
        os.system('ebook-convert {} {}'.format('books/' + title + ".epub", 'books/' + title + '.mobi'))
        bookname = 'books/' + title + '.mobi'

        upload_page = bookurl.replace('book', 'fileupload')
        print('uploading {} to {}'.format(bookname, bookurl))

        soup = BeautifulSoup(self.session.get(bookurl).text, 'lxml')
        token = soup.find("input", {"name":"csrfmiddlewaretoken"}).attrs['value']
        res = self.session.post(upload_page, data={'csrfmiddlewaretoken':token}, files={'doc':open(bookname, 'rb')})
        print('uploaded.')
        return True

    def shuffleUploadBooks(self):
        histories = json.load(open('uploaded.json', 'r'))
        rpage = 'https://readfree.me/rank/' + random.choice(['1', '7', '30', '365']) + '/?page=' + str(random.randint(1, 5))
        all_books = BeautifulSoup(self.session.get(rpage).text, 'lxml').findAll('a', {'class':'pjax'})
        rand_book = random.choice(all_books[0::2])
        bid = rand_book.attrs['href']+rand_book.img.attrs['alt']
        if bid in histories:
            self.shuffleUploadBooks()

        if self.uploadBook('https://readfree.me' + rand_book.attrs['href']):
            histories[bid] = max(histories.values()) + 1
            json.dump(histories, open('uploaded.json', 'w'), ensure_ascii=False, indent=2)


if __name__ == '__main__':
    rf = ReadFree('/usr/local/info/rfcookies.pkl', '/usr/local/info/readfree.json')
    rf.login()
    rf.shuffleUploadBooks()
    # rf.uploadBook('https://readfree.me/book/26734228/')

    # rf = ReadFree('/usr/local/info/ssruoz_rf.dat', '/usr/local/info/ssruoz_rf.json')    
    # print(arrow.now().format('YYYY-MM-DD HH-mm'))
    # pprint(rf.getAccountInfo())






