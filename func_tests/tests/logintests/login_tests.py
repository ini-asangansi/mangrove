# vim: ai ts=4 sts=4 et sw=4utf-8
from nose.plugins.attrib import attr
from framework.base_test import BaseTest
from framework.utils.data_fetcher import from_, fetch_
from pages.loginpage.login_page import LoginPage
from nose.plugins.skip import SkipTest
from testdata.test_data import DATA_WINNER_LOGIN_PAGE
from tests.logintests.login_data import *


class TestLoginPage(BaseTest):

    @attr('functional_test')
    def test_login_with_valid_credentials(self):
        self.driver.go_to(DATA_WINNER_LOGIN_PAGE)
        login_page = LoginPage(self.driver)

        dashboard_page = login_page.do_successful_login_with(VALID_CREDENTIALS)
        self.assertEqual(dashboard_page.welcome_message(),
            fetch_(WELCOME_MESSAGE, from_(VALID_CREDENTIALS)),
          "Login Un-successful or Welcome Message is not Present")

    @attr('functional_test')
    def test_login_with_unactivated_account_credentials(self):
        self.driver.go_to(DATA_WINNER_LOGIN_PAGE)
        login_page = LoginPage(self.driver)
        login_page.login_with(UNACTIVATED_ACCOUNT_CREDENTIALS)
        self.assertEqual(login_page.get_error_message(),
                         fetch_(ERROR_MESSAGE,
                                from_(UNACTIVATED_ACCOUNT_CREDENTIALS)))

    @attr('functional_test')
    def test_login_with_invalid_format_email_address(self):

        self.driver.go_to(DATA_WINNER_LOGIN_PAGE)
        login_page = LoginPage(self.driver)
        login_page.login_with(INVALID_EMAIL_ID_FORMAT)
        self.assertEqual(login_page.get_error_message(),
                         fetch_(ERROR_MESSAGE, from_(INVALID_EMAIL_ID_FORMAT)))

    @attr('functional_test')
    def test_login_with_invalid_password_credential(self):

        self.driver.go_to(DATA_WINNER_LOGIN_PAGE)
        login_page = LoginPage(self.driver)
        login_page.login_with(INVALID_PASSWORD)
        self.assertEqual(login_page.get_error_message(),
                         fetch_(ERROR_MESSAGE, from_(INVALID_PASSWORD)))

    @attr('functional_test')
    def test_login_without_entering_email_address(self):

        self.driver.go_to(DATA_WINNER_LOGIN_PAGE)
        login_page = LoginPage(self.driver)
        login_page.login_with(BLANK_EMAIL_ADDRESS)
        self.assertEqual(login_page.get_error_message(),
                         fetch_(ERROR_MESSAGE, from_(BLANK_EMAIL_ADDRESS)))

    @attr('functional_test')
    def test_login_without_entering_password(self):

        self.driver.go_to(DATA_WINNER_LOGIN_PAGE)
        login_page = LoginPage(self.driver)
        login_page.login_with(BLANK_PASSWORD)
        self.assertEqual(login_page.get_error_message(),
                         fetch_(ERROR_MESSAGE, from_(BLANK_PASSWORD)))

    @attr('functional_test')
    def test_login_without_entering_email_and_password(self):

        self.driver.go_to(DATA_WINNER_LOGIN_PAGE)
        login_page = LoginPage(self.driver)
        login_page.login_with(BLANK_CREDENTIALS)
        self.assertEqual(login_page.get_error_message(), fetch_(ERROR_MESSAGE,
                                                from_(BLANK_CREDENTIALS)))

    @attr('functional_test')
    def test_register_link_functionality(self):

        self.driver.go_to(DATA_WINNER_LOGIN_PAGE)
        login_page = LoginPage(self.driver)
        register_page = login_page.navigate_to_registration_page()
        self.assertEqual(register_page.get_title(), "Register")
