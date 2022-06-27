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

        # time.sleep(2)
        # log_out(self.browser)
        # registration(self.browser)
        # dialog_message = self.browser.find_element_by_xpath('//div[@class="swal-title"]')
        # time.sleep(2)
        # assert dialog_message.text == "Registration failed!"
        # print("2/b. Success!")

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
        edited_article_title = self.browser.find_element_by_xpath('//h1')

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
                   0] == "Valószerűtlennek tűnő, parányi élőlényt örökített meg Andreas Kay tudós az ecuadori esőerdő mélyén, ahol a világ talán legkülönösebb kinézetű ízeltlábúja rejtőzik. A Metagryne bicolumnata néven ismert kaszáspókféle meglehetősen aprócska, ugyanakkor igencsak feltűnő jelenség, hiszen feje (pontosabban előteste) leginkább egy kutyára emlékeztet."
        print("8. Success!")

    # 09. Adat törlése, egy cikk eltávolítása.
    # Ellenőrzés arra, hogy a cikk már nem található.

    def test_delete_article(self):
        login(self.browser, user["email"], user["password"])
        delete_article(self.browser)
        my_article = self.browser.find_elements_by_xpath(
            '//h1[text()="Kutyapók az erdő mélyén"]')

        assert len(my_article) == 0
        print("9. Success!")

    # 10. Ismételt és sorozatos adatbevitel adatforrásból, a profilkép lecserélése 5 alkalommal.
    # Ellenőrzés az aktuális kép megjelenésére.

    def test_input_from_file(self):
        login(self.browser, user["email"], user["password"])
        profile_pictures_list = ['https://i.pinimg.com/originals/af/37/54/af3754293e36740068bb6983aeb941d0.jpg',
                                 'https://i.pinimg.com/564x/3a/2b/3d/3a2b3d9d4e9e3e839cbd86347da949b4--funny-cats-funny-animals.jpg',
                                 'https://data.whicdn.com/images/353030664/original.jpg',
                                 'https://i.pinimg.com/736x/43/9e/fc/439efccb2ec86c2f17d69ef50d47c051.jpg',
                                 'https://i.pinimg.com/474x/30/95/33/30953317f40a9907fa5f5eac4353f6b6.jpg']
        for pictures in profile_pictures_list:
            actual_img = image_changes(self.browser, pictures)
            time.sleep(2)
            assert actual_img.get_attribute("src") == pictures
            print("10. Success!")

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
