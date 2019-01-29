import os
import requests
from urllib.request import urlretrieve, urlopen
from bs4 import BeautifulSoup
import pickle
import json
import re
from pprint import pprint

COOKIE_FILE = '/usr/local/info/rfcookies.dat'

class Readfree:
    def __init__(self, account_json='/usr/local/info/readfree.json'):
        self.account_json = account_json
        self.mainpage = "http://readfree.me"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Inter Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
            "Accppt": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*,q=0.8"}
        self.s = self.save_cookie_login()

    def is_login(self):
        # return either False or a session with cookie loaded
        if not os.path.exists(COOKIE_FILE):
            return False

        session = requests.Session()
        with open(cookie_path, 'rb') as f:
            cookies = pickle.load(f)
            cj = requests.cookies.RequestsCookieJar()
            cj._cookies = cookies
            session.cookies = cj
            session.headers = self.headers

        r_get = session.get(
            "http://readfree.me/accounts/profile/bluesea/wish/")
        if '/accounts/profile' in r_get.text:
            print("🕷  -- cookie remains valid.")
            return session
        else:
            return False

    def recognize_captcha(self, img):
        OCR().process(img)

    def load_account(self, accountJson):
        return json.load(open(accountJson, 'r'))

    def recognizeCaptcha(self, bsobj):
        ''' retrieve image from bsobj : beautiful soup object
        input: bs_obj
        output: string
        '''
        captcha = bsobj.find("img", {"class": "captcha"})
        text = ''
        if captcha:
            image_path = "images/captcha.jpg"
            urlretrieve(self.mainpage + captcha['src'], image_path)
            os.system("open images/captcha.jpg")
            text = input(">> Type in what u see: ").strip()
            # self.recognize_captcha(image_path)
        return text

    def save_cookie_login(self):
        ''' Log in account and localize cookies for further explorations.
        return logged session
        '''
        session = self.is_login()
        if session:
            return session

        dhost = "https://readfree.me/auth/login/?next=/"
        session = requests.Session()
        session.headers = self.headers
        r_get = session.get(dhost)
        account = self.load_account(self.account_json)

        bsobj = BeautifulSoup(r_get.text, 'lxml')
        csrftoken = bsobj.find("input", {"name":"csrfmiddlewaretoken"})['value']
        print(csrftoken, " >> 000")
        # return 
        captcha_0 = bsobj.find("input", {"name": "captcha_0"})["value"]
        captcha_1 = self.recognizeCaptcha(bsobj)
        # print(captcha_0, captcha_1)

        params = {
            'email': account['email'],
            'password': account['password'],
            'csrfmiddlewaretoken': csrftoken,
            'captcha_0': captcha_0,
            'captcha_1': captcha_1}
        r_post = session.post(dhost, data=params, headers=self.headers)
        print(r_post.text)

        if "/accounts/settings/" in r_post.text:
            print("LOGIN SUCCEED.")
            with open(COOKIE_FILE, 'wb') as f:
                pickle.dump(session.cookies._cookies, f)
        return session

    def get_account_info(self):
        ''' there are only few infos on each user
        return : username
        '''

        session = self.s
        soup = BeautifulSoup(session.get(self.mainpage).text, 'lxml')
        # print(soup)
        link = soup.find("a", href=re.compile(".*accounts/profile.*"))
        infos = []
        if link:
            infos.append(re.search(r'profile/(.*)/wish', str(link)).group(1))
            moresoup = BeautifulSoup(
                session.get(self.mainpage + link.attrs['href']).text, 'lxml')
            for item in moresoup.findAll('p', {"class": "muted"}):
                infos.append(item.text)

        return infos

    def parse_hot_books(self, pills=7):
        '''parse all the books on current pabe'''
        hot_page = self.mainpage + "/rank/" + str(pills)
        soup = BeautifulSoup(self.s.get(hot_page).text, 'lxml')
        for item in soup.findAll('div', {'class':'book-info'}):
            book_link = self.mainpage + item.find("a", {"class": "pjax"}).attrs['href']
            Aux().awesome_print(self.parse_single_book(book_link))
            print("\n")


    def parse_single_book(self, b_link):
        ''' parse info: book name, score ..
        :rtype: dictionary 
        '''
        infos = {}
        soup = BeautifulSoup(self.s.get(b_link).text, 'lxml')
        infos['name'] = soup.find('a', {"class":"link-search"}).text.strip()
        infos['author'] = soup.find('a', {"class":"z-link-search"}).text.strip()
        douban_link = soup.find('a', href=re.compile("http://book.douban.com/subject/.*"))
        infos['rate'] = Aux().douban_rate(douban_link.attrs['href']) if douban_link else 'DIY'
        infos['publisher'] = soup.find('small').text if douban_link else "None"
        infos['introduction'] = soup.find('pre').text
        infos['link'] = b_link
        return infos



    def delete_history(self, action, n=3):
        '''remvoe the most recent n book-ACTION(push, download, edit, comment) histories
        to delete all histories, set n to be a very large number, e.g., 9999
        action: push | down | edition | talk
        return: None
        '''
        username = self.get_account_info()[0]
        downpage = "http://readfree.me/accounts/profile/" + username + "/" + action
        session = self.save_cookie_login()
        soup = BeautifulSoup(
            session.get(
                downpage,
                headers=self.headers).text,
            'lxml')
        counter = 0

        # print(soup.text)
        regex = r"/" + re.escape(action) + r"/.*/delete"
        for item in soup.findAll('a', href=re.compile(regex)):
            regex = r"(/" + re.escape(action) + r"/.*/delete)"
            dellink = self.mainpage + re.search(regex, str(item)).group(1)
            print(dellink)

            if counter >= n:
                return
            session.get(dellink, headers=self.headers)
            counter += 1

        # Keep deleting rest n - counter histories
        if counter == 0:  # no more history
            return
        self.delete_history(action, n - counter)


class Aux:
    '''Auxiliary class containing methods for better readability 
    '''
    def check_contain_chinese(self, check_str):
        '''
        :itype: str
        :rtype: boolean 
        '''
        for ch in check_str:#.decode('utf-8'):
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False


    def awesome_print(self, bookinfos):
        '''
        :itype: dictionary
        :rtype: None
        '''
        chunk_size = 50 if self.check_contain_chinese(bookinfos['introduction']) else 100
        for k in sorted(bookinfos, key=len):
            v = bookinfos[k].replace("\n", "").replace("\r", "")
            if len(v) < chunk_size:
                print('{:<15}: {:<20}'.format(k, bookinfos[k]))
            else:
                print('{:<15}: {:<20}'.format(k, v[:chunk_size]))
                for i in range(chunk_size, len(v), chunk_size):
                    # print(v[i:i+chunk_size])
                    print('{:<15}  {:<20}'.format(' ', v[i:i+chunk_size]))


    def douban_rate(self, booklink):
        """ The rate and vote numbers are inaccurate from the original link
        :itype: url link 
        :rtype: str ([float, str].join(/))
        """
        try:
            soup = BeautifulSoup(requests.Session().get(booklink).text, 'lxml')
            rate = soup.find("strong", {"class": "ll rating_num "}).text.strip()
            vote = soup.find("a", {"class": "rating_people"}).text.strip()
            return str(rate) + " / " + vote
        except Exception as e:
            return "Not enough rate"




if __name__ == '__main__':
    rf = Readfree('/usr/local/info/readfree.json')
    rf.save_cookie_login()


# image_file = Image.open("images/captcha.jpg") # open colour image
# image_file = image_file.convert('1') # convert image to black and white
# image_file.save('result.jpg')
# img = Image.open("result.jpg")
# OCR().remove_noise(img,1)
# print(OCR().image_to_string(img))

# Readfree().recognize_captcha('images/result.jpg')
