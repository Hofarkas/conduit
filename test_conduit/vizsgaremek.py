from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from functions import login
from login_data import user
import time


# import csv


class TestConduit(object):
    def setup(self):
        browser_options = Options()
        browser_options.headless = True
        self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=browser_options)
        self.browser.implicitly_wait(10)
        URL = "http://localhost:1667/#/"
        self.browser.get(URL)

    def teardown(self):
        self.browser.quit()

# 01. Sütik elfogadása. Ellenőrzés a lista elem eltűnésére.

    def test_accept_cookies(self):
        accept_cookies_btn = self.browser.find_elements_by_xpath(
            '//button[@class="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')
        accept_cookies_btn[0].click()
        time.sleep(2)
        accept_cookies_btn = self.browser.find_elements_by_xpath(
            '//button[@class="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')

        assert len(accept_cookies_btn) == 0
        print("Success!")

# 02. Regisztráció negatív ágon invalid email-al. Ellenőrzés a hibaüzenet megjelenésére.

    # def test_invalid_registration(self):

# 03. Bejelentkezés valid adatokkal. Ellenőrzés a Log out megjelenésére.

    def test_login(self):
        login(self.browser, user["email"], user["password"])
        logout_btn = WebDriverWait(self.browser, 2).until(
            EC.presence_of_element_located((By.XPATH, '//a[@active-class="active"]')))

        assert logout_btn.is_displayed()
        print("Success!")

    # 04. XXX
    # 05. XXX
    # 06. XXX
    # 07. XXX
    # 08. XXX
    # 09. XXX
    # 10. XXX

# 11. Kijelentkezés. Ellenőrzés a fejlécen lévő Sign in megjelenésére.

    def test_logout(self):
        login(self.browser, user['email'], user['password'])
        time.sleep(2)
        logout_btn = self.browser.find_element_by_xpath('//a[@active-class="active"]')
        logout_btn.click()
        login_link_btn = WebDriverWait(self.browser, 2).until(
            EC.presence_of_element_located((By.XPATH, '//a[@href="#/login"]')))

        assert login_link_btn.is_displayed()
        print("Success!")
