from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pickle, time, sys, os, re, random
from bs4 import BeautifulSoup
import arrow 


COOKIE_FILE = "elena.pkl"
MAINPAGE = "https://www.hupu.com"
LOGINPAGE = "https://passport.hupu.com/pc/login"
SPURS = 'https://bbs.hupu.com/spurs'

class Bot():
    def __init__(self, cookie='wechat.pkl'):
        options = Options()
        for arg in (
            '--headless',
            '--disable-gpu',
            'window-size=1024,768',
            '--no-sandbox',
                'disable-infobars'):
            options.add_argument(arg)

        if  cookie:
            global COOKIE_FILE
            COOKIE_FILE = cookie
        self.driver = webdriver.Chrome(options=options)
        self.driver.set_page_load_timeout(130)

    def manual_login(self):
        # first time login
        print(">> You have 30 seconds to login. Chrome will exit automatically.")
        self.driver = webdriver.Chrome()
        self.driver.get(LOGINPAGE)
        try:
            element = WebDriverWait(
                self.driver, 30).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "hp-topbarNav-bd")))
            print("✔️  Login SUCCEED !")
            pickle.dump(self.driver.get_cookies(), open(COOKIE_FILE, "wb"))
        except Exception as e:
            print("☹️  Manual login timeout.")
            print(e)

    def login(self):
        ''': webdrive object
        '''
        if not os.path.exists(COOKIE_FILE):
            print(">> NO COOKIE WAS FOUND")
            self.manual_login()

        self.driver.get(LOGINPAGE)
        cookies = pickle.load(open(COOKIE_FILE, "rb"))
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        print(">> COOKIES LOADED/")
        self.driver.get(MAINPAGE)
        print(">> AUTO LOGIN SUCCEED/")
        return self.driver

    def bbs_rlights(self, url):
        self.driver.get(url)
        time.sleep(0.5)
        tid = 0
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        for idx, div in enumerate(soup.findAll('div', {'class':'floor_box '})):
            if div.a.text == 'Gentle3348':
                tid = idx 
                break
        rlks = self.driver.find_elements_by_class_name("ilike_icon")
        if rlks:
            rlks[tid].click()
        print(url, arrow.now())
        time.sleep(1)

    def rlights_replies(self):
        replypage = 'https://my.hupu.com/Elena_Greco_/topic-allreply-' + str(random.randint(1,6))
        self.driver.get(replypage)
        time.sleep(0.5)
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        repies = soup.findAll('a', href=re.compile(r'//bbs.hupu.com/.*\.html\#\d+'))

        print(COOKIE_FILE, arrow.now())
        for url in ['https:' + r.attrs['href'] for r in repies]:
            self.bbs_rlights(url)

def three_musketeers():
    for cf in ['mouse.pkl', 'bull.pkl', 'tiger.pkl', 'rabbit.pkl', 'elenaqq.pkl', 'wechat.pkl', 'alphablant.pkl', 'fivec.pkl', 'blutoqq.pkl']:
        try:
            b = Bot(cf)
            b.login()
            b.rlights_replies()
            b.driver.quit()
        except Exception as e:
            b.driver.quit()
            print(e)            
            # raise e



if __name__ == '__main__':
    while True:
        three_musketeers()
        time.sleep(600)


