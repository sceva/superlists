import time
import requests
from selenium.webdriver.support.ui import WebDriverWait
from .base import FunctionalTest

__author__ = 's'  # created on 3/11/14.

def get_new_persona_test_user():
    resp = requests.get('http://personatestuser.org/email')
    data = resp.json()
    return (data['email'], data['pass'])

test_email = get_new_persona_test_user()
EMAIL = test_email[0]
PASS = test_email[1]


class LoginTest(FunctionalTest):

    def test_login_with_persona(self):
        # Edith goes to the awesome superlists site
        # and notices a "Sign in" link for the first time
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_login').click()

        # A Persona login box appears
        self.switch_to_new_window('Mozilla Persona')

        # Edith logs in with her email address
        ## Use mockmyid.com for test email
        # self.browser.find_element_by_id(
        #     'authentication_email'
        # ).send_keys('edith@mockmyid.com')
        self.browser.find_element_by_id(
            'authentication_email'
        ).send_keys(EMAIL)
        self.browser.find_element_by_tag_name('button').click()

        self.wait_for_element_with_id('authentication_password')
        self.browser.find_element_by_id('authentication_password').send_keys(PASS)
        #self.browser.find_element_by_('isReturning.isTransitionToSecondary').click()

        buttons = self.browser.find_elements_by_tag_name('button')
        for button in buttons:
            if button.is_displayed():
                if 'sign in' in button.text:
                    button.click()
                    break

        # The Persona window closes
        self.switch_to_new_window('To-Do')

        # She can see that she is logged in
        self.wait_to_be_logged_in(email=EMAIL)

        # Refreshing the page, she sees it's a real session login
        # not just a one-off for that page
        self.browser.refresh()
        self.wait_to_be_logged_in(email=EMAIL)

        # Terrified of this new feature, she reflexively clicks logout
        self.browser.find_element_by_id('id_logout').click()
        self.wait_to_be_logged_out(email=EMAIL)

        # The 'logged out' status also persists after a refresh
        self.browser.refresh()
        self.wait_to_be_logged_out(email=EMAIL)

    def switch_to_new_window(self, text_in_title):
        retries = 60
        while retries > 0:
            for handle in self.browser.window_handles:
                self.browser.switch_to_window(handle)
                if text_in_title in self.browser.title:
                    return
            retries -= 1
            time.sleep(0.5)
        self.fail('could not find window')

