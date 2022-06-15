import time


def registration(browser, user_name, user_email, user_password):
    reg_link_btn = browser.find_element_by_xpath('//a[@href="#/register"]')
    reg_link_btn.click()
    reg_name_input = browser.find_element_by_xpath('//input[@placeholder="Username"]')
    reg_name_input.send_keys(user_name)
    reg_email_input = browser.find_element_by_xpath('//input[@placeholder="Email"]')
    reg_email_input.send_keys(user_email)
    reg_password_input = browser.find_element_by_xpath('//input[@type="password"]')
    reg_password_input.send_keys(user_password)
    sign_up_btn = browser.find_element_by_xpath('//button[@class="btn btn-lg btn-primary pull-xs-right"]')
    sign_up_btn.click()


def login(browser, user_email, user_password):
    login_link_btn = browser.find_element_by_xpath('//a[@href="#/login"]')
    login_link_btn.click()
    login_email_input = browser.find_element_by_xpath('//input[@placeholder="Email"]')
    login_email_input.send_keys(user_email)
    login_password_input = browser.find_element_by_xpath('//input[@type="password"]')
    login_password_input.send_keys(user_password)
    sign_in_btn = browser.find_element_by_xpath('//button[@class="btn btn-lg btn-primary pull-xs-right"]')
    sign_in_btn.click()


def find_ipsum_tag(browser):
    find_tag_ipsum = browser.find_element_by_xpath('//a[@href="#/tag/ipsum"]')
    find_tag_ipsum.click()


def create_new_article(browser, title_input, about_input, main_input, tag_input):
    new_article_btn = browser.find_element_by_xpath('//a[@href="#/editor"]')
    new_article_btn.click()
    new_article_title_input = browser.find_element_by_xpath('//input[@type="text"]')
    new_article_title_input.send_keys(title_input)
    new_article_about_input = browser.find_element_by_xpath('//input[@class="form-control"]')
    new_article_about_input.send_keys(about_input)
    new_article_main_input = browser.find_element_by_xpath('//textarea[@placeholder="Write your article (in markdown)"]')
    new_article_main_input.send_keys(main_input)
    new_article_tag_input = browser.find_element_by_xpath('//input[@placeholder="Enter tags"]')
    new_article_tag_input.send_keys(tag_input)
    publish_article_btn = browser.find_element_by_xpath('//button[@class="btn btn-lg pull-xs-right btn-primary"]')
    publish_article_btn.click()
