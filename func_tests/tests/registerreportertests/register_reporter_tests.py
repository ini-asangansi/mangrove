# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from nose.plugins.attrib import attr

from framework.base_test import BaseTest
from framework.utils.data_fetcher import fetch_, from_
from pages.loginpage.login_page import LoginPage
from pages.registerreporterpage.register_reporter_page import ReporterRegistrationPage
from testdata.test_data import DATA_WINNER_LOGIN_PAGE
from tests.logintests.login_data import VALID_CREDENTIALS
from tests.registerreportertests.register_reporter_data import VALID_DATA, SUCCESS_MSG, BLANK_FIELDS, ERROR_MSG


class TestRegisterReporter(BaseTest):

    @attr('functional_test')
    def test_successful_registration_of_reporter(self):
        """
        Function to test the successful registration of reporter with given
        details e.g. first name, last name, telephone number and commune
        """
        # doing successful login with valid credentials
        self.driver.go_to(DATA_WINNER_LOGIN_PAGE)
        login_page = LoginPage(self.driver)
        dashboard_page = login_page.do_successful_login_with(VALID_CREDENTIALS)

        # doing reporter registration
        register_reporter_page = dashboard_page.navigate_to_register_reporter_page()

        register_reporter_page.register_with(VALID_DATA)
        self.assertRegexpMatches(register_reporter_page.get_success_message(),
                                 fetch_(SUCCESS_MSG, from_(VALID_DATA)))

    @attr('functional_test')
    def test_registration_of_reporter_without_entering_data(self):
        """
        Function to test the successful registration of reporter with given
        details e.g. first name, last name, telephone number and commune
        """
        # doing successful login with valid credentials
        self.driver.go_to(DATA_WINNER_LOGIN_PAGE)
        login_page = LoginPage(self.driver)
        dashboard_page = login_page.do_successful_login_with(VALID_CREDENTIALS)

        # doing reporter registration
        register_reporter_page = dashboard_page.navigate_to_register_reporter_page()

        register_reporter_page.register_with(BLANK_FIELDS)
        self.assertEqual(register_reporter_page.get_error_message(),
                                 fetch_(ERROR_MSG, from_(BLANK_FIELDS)))
