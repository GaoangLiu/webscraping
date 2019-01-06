from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pickle, time, sys, os, re, random
from bs4 import BeautifulSoup


COOKIE_FILE = "12306.pkl"
MAINPAGE = "https://www.12306.cn/index/"
LOGINPAGE = "https://kyfw.12306.cn/otn/resources/login.html"
SPURS = 'https://bbs.hupu.com/spurs'

class Train():
    def __init__(self):
        options = Options()
        for arg in (
            # '--headless',
            '--disable-gpu',
            'window-size=1024,768',
            '--no-sandbox',
            'disable-infobars'):
            options.add_argument(arg)
        self.driver = webdriver.Chrome(options=options)
        # self.driver.set_page_load_timeout(30)

    def manual_login(self):
        # first time login
        print("📧 You have 30 seconds to login. Do NOT close chrome manually, it will exit automatically !!")
        self.driver = webdriver.Chrome()
        self.driver.get(LOGINPAGE)
        try:
            element = WebDriverWait(
                self.driver, 60).until(
                EC.presence_of_element_located(
                    (By.ID, "J-header-logout")))
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
        time.sleep(3)
        cookies = pickle.load(open(COOKIE_FILE, "rb"))
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        print(">> Cookies loaded")
        self.driver.get(MAINPAGE)
        print(">> Auto Login DONE")
        time.sleep(50)
        return self.driver


t = Train()
try:
    t.login()
except Exception as e:
    print(e)

t.driver.quit()




