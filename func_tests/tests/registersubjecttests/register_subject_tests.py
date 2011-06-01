# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from nose.plugins.attrib import attr
from nose.plugins.skip import SkipTest
from framework.base_test import BaseTest
from framework.utils.data_fetcher import fetch_, from_
from pages.loginpage.login_page import LoginPage
from pages.registersubjectpage.register_subject_page import RegisterSubjectPage
from testdata.test_data import DATA_WINNER_LOGIN_PAGE
from tests.logintests.login_data import VALID_CREDENTIALS
from tests.logintests.login_tests import TestLoginPage
from tests.registersubjecttests.register_subject_data import VALID_DATA, SUCCESS_MSG, ERROR_MSG


class TestRegisterSubject(BaseTest):

    def prerequisites_of_register_subject(self):
        # doing successful login with valid credentials
        self.driver.go_to(DATA_WINNER_LOGIN_PAGE)
        login_page = LoginPage(self.driver)
        dashboard_page = login_page.do_successful_login_with(VALID_CREDENTIALS)
        return dashboard_page.navigate_to_register_subject_page()
    @SkipTest
    @attr('functional_test', 'smoke')
    def test_successful_registration_of_subject(self):
        """
        Function to test the successful registration of subject with given
        details
        """
        register_subject_page = self.prerequisites_of_register_subject()
        message = register_subject_page.successfully_register_subject_with(VALID_DATA)
        self.assertRegexpMatches(register_subject_page.get_flash_message(), message)
    @SkipTest
    @attr('functional_test')
    def test_registration_of_subject_without_entering_data(self):
        """
        Function to test the successful registration of subject with given
        details e.g. first name, last name, telephone number and commune
        """
        register_subject_page = self.prerequisites_of_register_subject()
        register_subject_page.register_with(BLANK_FIELDS)
        self.assertEqual(register_subject_page.get_error_message(),
                                 fetch_(ERROR_MSG, from_(BLANK_FIELDS)))
