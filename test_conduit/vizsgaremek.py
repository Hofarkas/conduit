from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from functions import *
from login_data import user
from article_data import article, edit_article
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

    # 01. Sütik elfogadása.
    # Ellenőrzés a lista elem eltűnésére.

    def test_accept_cookies(self):
        accept_cookies_btn = self.browser.find_elements_by_xpath(
            '//button[@class="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')
        accept_cookies_btn[0].click()
        time.sleep(2)
        accept_cookies_btn = self.browser.find_elements_by_xpath(
            '//button[@class="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')

        assert len(accept_cookies_btn) == 0
        print("1. Success!")

    # 02. Regisztráció negatív ágon már regisztrált email-al.
    # Ellenőrzés a hibaüzenet megjelenésére.

    def test_invalid_registration(self):
        registration(self.browser, user["username"], user["email"], user["password"])
        error_message = self.browser.find_element_by_xpath('//button[@class="swal-button swal-button--confirm"]')

        assert error_message.is_displayed()
        print("2. Success!")
        error_message.click()

    # 03. Bejelentkezés helyesen megadott adatokkal.
    # Ellenőrzés a Log out megjelenésére.

    def test_login(self):
        login(self.browser, user["email"], user["password"])
        logout_btn = WebDriverWait(self.browser, 2).until(
            EC.presence_of_element_located((By.XPATH, '//a[@active-class="active"]')))

        assert logout_btn.is_displayed()
        print("3. Success!")

    # 04. Adatok, az összes "lorem" taggel ellátott cikk kilistázása.
    # Ellenőrzés a #lorem megjelenésére.

    def test_find_ipsum_tag(self):
        login(self.browser, user["email"], user["password"])
        find_ipsum_tag(self.browser)
        lorem_hashtag = WebDriverWait(self.browser, 2).until(
            EC.presence_of_element_located((By.XPATH, '//a[@class="nav-link router-link-exact-active active"]')))

        assert lorem_hashtag.is_displayed()
        print("4. Success!")

    # 05. Több oldalas lista bejárás, a cikkek végiglapozása a kezdőoldalon.
    # Ellenőrzés az aktuális oldalra.

    def test_pagination(self):
        login(self.browser, user["email"], user["password"])
        page_list = self.browser.find_elements_by_xpath('//a[@class="page-link"]')
        for page in page_list:
            page.click()
            actual_page = self.browser.find_element_by_xpath('//li[@class="page-item active"]')

            assert page.text in actual_page.text
        print("5. Success!")

    # 06. Új adat bevitel, egy új cikk létrehozása.
    # Ellenőrzés a cikk címének megjelenésére.

    def test_create_new_article(self):
        login(self.browser, user["email"], user["password"])
        create_new_article(self.browser, article["title"], article["about"], article["main"], article["tag"])
        article_title = self.browser.find_element_by_xpath('//h1')

        assert article_title.text == article["title"]
        print("6. Success!")

    # 07. Meglévő adat módosítása, egy cikk címének szerkesztése.
    # Ellenőrzés az új cím megjelenésére.

    def test_edit_article(self):
        login(self.browser, user["email"], user["password"])
        editing_article(self.browser, edit_article["new_title"])
        edited_article_title = self.browser.find_element_by_xpath('//h1')

        assert edited_article_title.text == "Kutyapók az erdő mélyén"
        print("7. Success!")

    # 08. Adat törlése, egy cikk eltávolítása.
    # Ellenőrzés

    # def test_delete_article(self):
    #     login(self.browser, user["email"], user["password"])

    # 09. Adatok lementése felületről.
    # Ellenőrzés

    # 10. Ismételt és sorozatos adatbevitel adatforrásból.
    # Ellenőrzés

    # 11. Kijelentkezés. Ellenőrzés a fejlécen lévő Sign in megjelenésére.

    def test_logout(self):
        login(self.browser, user['email'], user['password'])
        time.sleep(2)
        logout_btn = self.browser.find_element_by_xpath('//a[@active-class="active"]')
        logout_btn.click()
        login_link_btn = WebDriverWait(self.browser, 2).until(
            EC.presence_of_element_located((By.XPATH, '//a[@href="#/login"]')))

        assert login_link_btn.is_displayed()
        print("11. Success!")
