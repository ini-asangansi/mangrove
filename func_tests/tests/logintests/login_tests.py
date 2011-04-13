# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from framework.base_test import BaseTest
from framework.pages.loginpage.login_page import LoginPage
from nose.tools import *
from nose.plugins.skip import SkipTest
from framework.utils.data_fetcher import *
from tests.logintests.login_data import *

__author__ = 'kumarr'

#@SkipTest
class TestLoginPage(BaseTest):


    def test_login_with_valid_credentials(self):
        self.driver.get("http://localhost:8000/login")
        login_page = LoginPage(self.driver)

        dashboard_page= login_page.login_with(VALID_CREDENTIALS)
        eq_(dashboard_page.welcome_message(),
            fetch_(WELCOME_MESSAGE, from_(VALID_CREDENTIALS)),
          "Login Un-successful or Welcome Message is not Present")


    def test_login_with_unactivated_account_credentials(self):
        self.driver.get("http://localhost:8000/login")
        login_page = LoginPage(self.driver)

        login_page.login_with(UNACTIVATED_ACCOUNT_CREDENTIALS)
        eq_(login_page.error_message(), fetch_(ERROR_MESSAGE, from_(UNACTIVATED_ACCOUNT_CREDENTIALS)),
          "Error Message for Un-Activated Accounts is not present.")


    def test_login_with_invalid_format_email_address(self):

        self.driver.get("http://localhost:8000/login")
        login_page = LoginPage(self.driver)
        login_page.login_with(INVALID_EMAIL_ID_FORMAT)
        eq_(login_page.error_message(), fetch_(ERROR_MESSAGE, from_(INVALID_EMAIL_ID_FORMAT)), "Error Message for Invalid Format Email Address is not present.")


    def test_login_with_invalid_password_credential(self):

        self.driver.get("http://localhost:8000/login")
        login_page = LoginPage(self.driver)
        login_page.login_with(INVALID_PASSWORD)
        eq_(login_page.error_message(), fetch_(ERROR_MESSAGE, from_(INVALID_PASSWORD)), "Error Message for Invalid Password is not present.")



    def test_login_without_entering_email_address(self):

        self.driver.get("http://localhost:8000/login")
        login_page = LoginPage(self.driver)
        login_page.login_with(BLANK_EMAIL_ADDRESS)
        eq_(login_page.error_message(),fetch_(ERROR_MESSAGE, from_(BLANK_EMAIL_ADDRESS)), "Error Message for Blank EMail Textbox is not present.")



    def test_login_without_entering_password(self):

        self.driver.get("http://localhost:8000/login")
        login_page = LoginPage(self.driver)
        login_page.login_with(BLANK_PASSWORD)
        eq_(login_page.error_message(), fetch_(ERROR_MESSAGE, from_(BLANK_PASSWORD)), "Error Message for Blank Password Textbox is not present.")


    def test_login_without_entering_email_and_password(self):

        self.driver.get("http://localhost:8000/login")
        login_page = LoginPage(self.driver)
        login_page.login_with(BLANK_CREDENTIALS)
        eq_(login_page.get_error_message(),fetch_(ERROR_MESSAGE, from_(BLANK_CREDENTIALS)), "Error Message for Blank Password Textbox is not present.")

    def test_register_link_functionality(self):

        self.driver.get("http://localhost:8000/login")
        login_page = LoginPage(self.driver)
        register_page=login_page.navigate_to_registration_page()
        eq_(register_page.get_title(), "Register", "Registration Page Title is incorrect or Register Link is Not Working")



