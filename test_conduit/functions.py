# import time


def login(browser, user_email, user_password):
    login_link_btn = browser.find_element_by_xpath('//a[@href="#/login"]')
    login_link_btn.click()
    login_email_input = browser.find_element_by_xpath('//input[@placeholder="Email"]')
    login_email_input.send_keys(user_email)
    login_password_input = browser.find_element_by_xpath('//input[@type="password"]')
    login_password_input.send_keys(user_password)
    sign_in_btn = browser.find_element_by_xpath('//button[@class="btn btn-lg btn-primary pull-xs-right"]')
    sign_in_btn.click()
