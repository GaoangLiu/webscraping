from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pickle, time, sys, os, re, random
from bs4 import BeautifulSoup


COOKIE_FILE = "alphablant.pkl"
MAINPAGE = "https://www.hupu.com"
LOGINPAGE = "https://passport.hupu.com/pc/login"
SPURS = 'https://bbs.hupu.com/spurs'

class Hupu():
    def __init__(self):
        options = Options()
        for arg in (
            # '--headless',
            '--disable-gpu',
            # 'window-size=1024,768',
            '--no-sandbox',
                'disable-infobars'):
            options.add_argument(arg)
        self.driver = webdriver.Chrome(options=options)
        self.driver.set_page_load_timeout(120)

    def manual_login(self):
        # first time login
        print("📧 You have 30 seconds to login. Do NOT close chrome manually, it will exit automatically !!")
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
            print(
                ">> No cookie was found, you should login with Chrome-Browser for at least once.")
            self.manual_login()

        self.driver.get(LOGINPAGE)
        cookies = pickle.load(open(COOKIE_FILE, "rb"))
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        print(">> Cookies loaded")
        self.driver.get(MAINPAGE)
        print(">> Auto Login DONE")
        return self.driver

    def post_notes(self, content):
        # post 碎碎念
        self.driver.get("https://my.hupu.com/")
        self.driver.find_element_by_id('note_post').send_keys(content)
        self.driver.find_element_by_id('note_btn').click()

    def post_reply(self, url, commentary):
        # post commentary to a bbs page
        self.driver.get(url)
        time.sleep(10)
        try:
            self.driver.find_element_by_id('atc_content').send_keys(commentary)
            self.driver.find_element_by_id('fbd_reply_note').click()
            self.driver.find_element_by_id('fastbtn').send_keys(Keys.RETURN)
        except Exception as e:
            print(e)
            print('post reply failed')

    def get_bbs_address(self):
        self.driver.get("https://bbs.hupu.com")
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        links = [l.attrs['href'] for l in soup.findAll('a', href=re.compile(r'^/\d+.html'))]
        return "https://bbs.hupu.com" + random.choice(links[1::])


    def copy_reply(self, url):
        self.driver.get(url)
        soup = BeautifulSoup(self.driver.page_source, 'lxml')        
        # soup = BeautifulSoup(open('1bbs.html', 'rb').read(), 'lxml')
        replies = []
        for e in soup.findAll('td'):
            text = e.text.strip()
            text = re.sub(r'引用.*发表的:', '', text)
            text = re.sub(r'发自.*', '', text)
            replies.append(text)

        return random.choice(replies[2::])

    def water_bbs(self):
        url = self.get_bbs_address()
        commentary = self.copy_reply(url)
        self.post_reply(url, commentary)

    def bbs_rlights(self):
        url = 'https://bbs.hupu.com/25110537-12.html#84875'
        self.driver.get(url)
        time.sleep(0.5)
        tid = 0
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        for idx, div in enumerate(soup.findAll('div', {'class':'floor_box '})):
            if div.a.text == 'EIenaGreco':
                tid = idx 
                break
        time.sleep(5)
        rlks = self.driver.find_elements_by_class_name("ilike_icon")
        rlks[tid].click()
        # print(self.driver.page_source)






