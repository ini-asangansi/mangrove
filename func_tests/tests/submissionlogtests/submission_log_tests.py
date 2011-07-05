# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
import time
from nose.plugins.attrib import attr
from nose.plugins.skip import SkipTest
from framework.base_test import BaseTest
from framework.utils.data_fetcher import fetch_, from_
from pages.loginpage.login_page import LoginPage
from pages.smstesterpage.sms_tester_page import SMSTesterPage
from pages.submissionlogpage.submission_log_page import SubmissionLogPage
from testdata.test_data import DATA_WINNER_SUBMISSION_LOG_PAGE, DATA_WINNER_SMS_TESTER_PAGE, DATA_WINNER_LOGIN_PAGE, DATA_WINNER_HOME_PAGE
from tests.logintests.login_data import VALID_CREDENTIALS, WELCOME_MESSAGE
from tests.smstestertests.sms_tester_data import *
from tests.submissionlogtests.submission_log_data import *


class TestSubmissionLog(BaseTest):

    def prerequisites_of_submission_log(self, sms_data):
        self.driver.go_to(DATA_WINNER_LOGIN_PAGE)
        login_page = LoginPage(self.driver)
        dashboard_page = login_page.do_successful_login_with(VALID_CREDENTIALS)
        self.assertEqual(dashboard_page.welcome_message(),
            fetch_(WELCOME_MESSAGE, from_(VALID_CREDENTIALS)))
        self.driver.go_to(DATA_WINNER_SMS_TESTER_PAGE)
        sms_tester_page = SMSTesterPage(self.driver)
        sms_tester_page.send_sms_with(sms_data)
        self.assertEqual(sms_tester_page.get_response_message(), fetch_(MESSAGE, from_(sms_data)))
        self.driver.go_to(DATA_WINNER_HOME_PAGE)
        view_all_project_page = dashboard_page.navigate_to_view_all_project_page()
        time.sleep(3)
        project_overview_project = view_all_project_page.navigate_to_project_page(PROJECT_NAME)
        time.sleep(3)
        data_page = project_overview_project.navigate_to_data_page()
        time.sleep(3)
        submission_log_page = data_page.navigate_to_all_data_record_page()
        return submission_log_page

    @attr('functional_test', 'smoke')
    def test_verify_successful_sms_submission_log(self):
        """
        Function to test the successful SMS submission
        """
        submission_log_page = self.prerequisites_of_submission_log(VALID_DATA2)
        time.sleep(3)
        self.assertRegexpMatches(submission_log_page.get_submission_message(SMS_DATA_LOG), fetch_(SMS_SUBMISSION, from_(SMS_DATA_LOG)))

    @attr('functional_test')
    def test_invalid_sms_submission_log(self):
        """
        Function to test the invalid SMS submission by exceeding value of the word field limit
        """
        submission_log_page = self.prerequisites_of_submission_log(EXCEED_NAME_LENGTH2)
        time.sleep(3)
        self.assertRegexpMatches(submission_log_page.get_submission_message(EXCEED_WORD_LIMIT_LOG), fetch_(SMS_SUBMISSION, from_(EXCEED_WORD_LIMIT_LOG)))
        self.assertEqual(submission_log_page.get_failure_message(EXCEED_WORD_LIMIT_LOG), fetch_(FAILURE_MSG, from_(EXCEED_WORD_LIMIT_LOG)))

    @attr('functional_test')
    def test_submission_log_for_extra_plus_in_btw_sms(self):
        """
        Function to test the successful SMS submission while using extra plus in between of SMS
        """
        submission_log_page = self.prerequisites_of_submission_log(EXTRA_PLUS_IN_BTW)
        time.sleep(3)
        self.assertRegexpMatches(submission_log_page.get_submission_message(EXTRA_PLUS_IN_BTW_LOG), fetch_(SMS_SUBMISSION, from_(EXTRA_PLUS_IN_BTW_LOG)))

    @attr('functional_test')
    def test_submission_log_for_invalid_geo_code_format(self):
        """
        Function to test the invalid SMS submission for invalid geo code
        """
        submission_log_page = self.prerequisites_of_submission_log(WITH_INVALID_GEO_CODE_FORMAT)
        time.sleep(3)
        self.assertRegexpMatches(submission_log_page.get_submission_message(WITH_INVALID_GEO_CODE_FORMAT_LOG), fetch_(SMS_SUBMISSION, from_(WITH_INVALID_GEO_CODE_FORMAT_LOG)))
        self.assertEqual(submission_log_page.get_failure_message(WITH_INVALID_GEO_CODE_FORMAT_LOG), fetch_(FAILURE_MSG, from_(WITH_INVALID_GEO_CODE_FORMAT_LOG)))
