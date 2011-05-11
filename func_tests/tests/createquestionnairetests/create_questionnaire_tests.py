# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from nose.plugins.attrib import attr
from nose.plugins.skip import SkipTest
from framework.base_test import BaseTest
from framework.utils.data_fetcher import fetch_, from_
from pages.loginpage.login_page import LoginPage
from pages.createquestionnairepage.create_questionnaire_page import CreateQuestionnairePage
from testdata.test_data import DATA_WINNER_LOGIN_PAGE
from tests.logintests.login_data import VALID_CREDENTIALS
from tests.createquestionnairetests.create_questionnaire_data import *


class TestCreateQuestionnaire(BaseTest):

    def prerequisites_of_create_questionnaire(self):
        # doing successful login with valid credentials
        self.driver.go_to(DATA_WINNER_LOGIN_PAGE)
        login_page = LoginPage(self.driver)
        dashboard_page = login_page.do_successful_login_with(VALID_CREDENTIALS)

        # going on setup project page
        return dashboard_page.navigate_to_create_questionnaire_page()
    @SkipTest
    @attr('functional_test')
    def test_successful_questionnaire_creation(self):
        """
        Function to test the successful registration of reporter with given
        details e.g. first name, last name, telephone number and commune
        """
        create_questionnaire_page = self.prerequisites_of_create_questionnaire()
        create_questionnaire_page.create_questionnaire_with(VALID_DATA)
        self.assertRegexpMatches(register_reporter_page.get_success_message(),
                                 fetch_(PAGE_TITLE, from_(VALID_DATA)))
    @SkipTest
    @attr('functional_test')
    def test_registration_of_reporter_without_entering_data(self):
        """
        Function to test the successful registration of reporter with given
        details e.g. first name, last name, telephone number and commune
        """
        register_reporter_page = self.prerequisites_of_register_reporter()
        register_reporter_page.register_with(BLANK_FIELDS)
        self.assertEqual(register_reporter_page.get_error_message(),
                                 fetch_(ERROR_MSG, from_(BLANK_FIELDS)))
