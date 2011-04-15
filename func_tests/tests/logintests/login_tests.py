# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from framework.base_test import BaseTest
from pages.loginpage.login_page import LoginPage
from nose.plugins.skip import SkipTest
from framework.utils.data_fetcher import *
from testdata.test_data import DATA_WINNER_WEBSITE
from tests.logintests.login_data import *

@SkipTest
class TestLoginPage(BaseTest):


    def test_login_with_valid_credentials(self):
        self.driver.get(DATA_WINNER_WEBSITE)
        login_page = LoginPage(self.driver)

        dashboard_page= login_page.do_successful_login_with(VALID_CREDENTIALS)
        self.assertEqual(dashboard_page.welcome_message(),
            fetch_(WELCOME_MESSAGE, from_(VALID_CREDENTIALS)),
          "Login Un-successful or Welcome Message is not Present")


    def test_login_with_unactivated_account_credentials(self):
        self.driver.go_to(DATA_WINNER_WEBSITE)
        login_page = LoginPage(self.driver)
        login_page.login_with(UNACTIVATED_ACCOUNT_CREDENTIALS)
        self.assertEqual(login_page.get_error_message(), fetch_(ERROR_MESSAGE,
                                           from_(UNACTIVATED_ACCOUNT_CREDENTIALS)))


    def test_login_with_invalid_format_email_address(self):

        self.driver.go_to(DATA_WINNER_WEBSITE)
        login_page = LoginPage(self.driver)
        login_page.login_with(INVALID_EMAIL_ID_FORMAT)
        self.assertEqual(login_page.get_error_message(),
                         fetch_(ERROR_MESSAGE, from_(INVALID_EMAIL_ID_FORMAT)))


    def test_login_with_invalid_password_credential(self):

        self.driver.go_to(DATA_WINNER_WEBSITE)
        login_page = LoginPage(self.driver)
        login_page.login_with(INVALID_PASSWORD)
        self.assertEqual(login_page.get_error_message(), fetch_(ERROR_MESSAGE, from_(INVALID_PASSWORD)))



    def test_login_without_entering_email_address(self):

        self.driver.go_to(DATA_WINNER_WEBSITE)
        login_page = LoginPage(self.driver)
        login_page.login_with(BLANK_EMAIL_ADDRESS)
        self.assertEqual(login_page.get_error_message(),
                         fetch_(ERROR_MESSAGE, from_(BLANK_EMAIL_ADDRESS)))



    def test_login_without_entering_password(self):

        self.driver.go_to(DATA_WINNER_WEBSITE)
        login_page = LoginPage(self.driver)
        login_page.login_with(BLANK_PASSWORD)
        self.assertEqual(login_page.get_error_message(),
                         fetch_(ERROR_MESSAGE, from_(BLANK_PASSWORD)))


    def test_login_without_entering_email_and_password(self):

        self.driver.go_to(DATA_WINNER_WEBSITE)
        login_page = LoginPage(self.driver)
        login_page.login_with(BLANK_CREDENTIALS)
        self.assertEqual(login_page.get_error_message(),fetch_(ERROR_MESSAGE,
                                                from_(BLANK_CREDENTIALS)))

    def test_register_link_functionality(self):

        self.driver.go_to(DATA_WINNER_WEBSITE)
        login_page = LoginPage(self.driver)
        register_page=login_page.navigate_to_registration_page()
        self.assertEqual(register_page.get_title(), "Register")



