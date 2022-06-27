from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from functions import *
from login_data import user
from article_data import article, edit_article
import time


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

    # 02. Regisztráció negatív ágon.
    # Ellenőrzés a hibaüzenet megjelenésére.

    def test_invalid_registration(self):
        registration(self.browser)
        ok_btn = self.browser.find_element_by_xpath('//button[@class="swal-button swal-button--confirm"]')
        ok_btn.click()
        time.sleep(2)
        name = self.browser.find_element_by_xpath('//a[@href="#/@Tesztelek/"]')
        assert name.is_displayed()
        print("2/a. Success!")

        time.sleep(2)
        log_out(self.browser)
        registration(self.browser)
        dialog_message = self.browser.find_element_by_xpath('//div[@class="swal-title"]')
        time.sleep(2)
        assert dialog_message.text == "Registration failed!"
        print("2/b. Success!")

    # 03. Bejelentkezés helyesen megadott adatokkal.
    # Ellenőrzés a Log out megjelenésére.

    def test_login(self):
        login(self.browser, user["email"], user["password"])
        logout_btn = WebDriverWait(self.browser, 2).until(
            EC.presence_of_element_located((By.XPATH, '//a[@active-class="active"]')))

        assert logout_btn.is_displayed()
        print("3. Success!")

    # 04. Adatok, az összes "lorem" taggel ellátott cikk kilistázása.
    # Ellenőrzés az ipsum tegű cikkek számára.

    def test_find_ipsum_tag(self):
        login(self.browser, user["email"], user["password"])
        find_ipsum_tag(self.browser)
        time.sleep(5)
        ipsum_article = self.browser.find_elements_by_xpath('//div[@class="article-preview"]')

        assert len(ipsum_article) == 3
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
        article_titles = self.browser.find_elements_by_xpath('//h1')
        for article_item in article_titles:
            print(article_item.text)

        assert article_titles[0].text == article["title"]
        print("6. Success!")

    # 07. Meglévő adat módosítása, egy cikk címének szerkesztése.
    # Ellenőrzés az új cím megjelenésére.

    def test_edit_article(self):
        login(self.browser, user["email"], user["password"])
        editing_article(self.browser, edit_article["new_title"])
        edited_article_title = WebDriverWait(self.browser, 2).until(
            EC.presence_of_element_located((By.XPATH, '//h1')))

        assert edited_article_title.text == "Kutyapók az erdő mélyén"
        print("7. Success!")

    # 08. Adatok, a saját cikk tartalmának lementése felületről.
    # Ellenőrzés a tartalom txt-ben lévő megjelenésére.

    def test_save_data(self):
        login(self.browser, user["email"], user["password"])
        save_data(self.browser)
        my_article = self.browser.find_element_by_xpath(
            '//h1[text()="Kutyapók az erdő mélyén"]')
        my_article.click()
        time.sleep(2)
        article_main = self.browser.find_element_by_xpath('//div[@class="col-xs-12"]/div/p')
        with open("./article_main.txt", "w", encoding='UTF-8') as file:
            file.write(article_main.text)

        with open("./article_main.txt", "r", encoding='UTF-8') as file:
            content = file.readlines()

        assert content[
                   0] == "Parányi élőlényt örökített meg, ami leginkább egy kutyára emlékeztet."
        print("8. Success!")

    # 09. Ismételt és sorozatos adatbevitel adatforrásból, a profilkép lecserélése 5 alkalommal.
    # Ellenőrzés a kiküldött kommentek számára.

    def test_input_from_file(self):
        login(self.browser, user["email"], user["password"])
        time.sleep(2)
        my_article = self.browser.find_elements_by_xpath('//h1')
        my_article_text = my_article[1].text
        my_article[1].click()
        time.sleep(2)
        article_name = self.browser.find_element_by_xpath('//div[@class="container"]/h1')
        assert my_article_text == article_name.text
        comment_textarea = self.browser.find_element_by_xpath('//div[@class="card-block"]/textarea')
        comment_submit_button = self.browser.find_element_by_xpath('//button[@class="btn btn-sm btn-primary"]')
        with open("comments.txt", "r", encoding='UTF-8') as file:
            file_row_count = len(file.readlines())
            file.seek(0)
            for line in file.readlines():
                comment_textarea.clear()
                comment_textarea.send_keys(line)
                comment_submit_button.click()
        time.sleep(2)
        comments = self.browser.find_elements_by_xpath('//div[@class="card"]')
        assert len(comments) == file_row_count
        print("10. Success!")

    # 10. Adat törlése, egy cikk eltávolítása.
    # Ellenőrzés arra, hogy a cikk már nem található.

    def test_delete_article(self):
        login(self.browser, user["email"], user["password"])
        delete_article(self.browser)
        my_article = self.browser.find_elements_by_xpath(
            '//h1[text()="Kutyapók az erdő mélyén"]')

        assert len(my_article) == 0
        print("9. Success!")

    # 11. Kijelentkezés.
    # Ellenőrzés a fejlécen lévő Sign in megjelenésére.

    def test_logout(self):
        login(self.browser, user['email'], user['password'])
        time.sleep(2)
        log_out(self.browser)
        login_link_btn = WebDriverWait(self.browser, 2).until(
            EC.presence_of_element_located((By.XPATH, '//a[@href="#/login"]')))

        assert login_link_btn.is_displayed()
        print("11. Success!")
