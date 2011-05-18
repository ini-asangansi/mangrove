# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
import time
from nose.plugins.attrib import attr
from nose.plugins.skip import SkipTest
from framework.base_test import BaseTest
from framework.utils.data_fetcher import fetch_, from_
from pages.loginpage.login_page import LoginPage
from pages.smstesterpage.sms_tester_page import SMSTesterPage
from pages.submissionlogpage.submission_log_page import SubmissionLogPage
from testdata.test_data import DATA_WINNER_SUBMISSION_LOG_PAGE, DATA_WINNER_SMS_TESTER_PAGE, DATA_WINNER_LOGIN_PAGE
from tests.logintests.login_data import VALID_CREDENTIALS, WELCOME_MESSAGE
from tests.smstestertests.sms_tester_data import VALID_DATA2, MESSAGE, EXCEED_NAME_LENGTH2
from tests.submissionlogtests.submission_log_data import *


class TestSubmissionLog(BaseTest):

    test_var = None

    def prerequisites_of_submission_log(self, sms_data):
        self.driver.go_to(DATA_WINNER_LOGIN_PAGE)
        login_page = LoginPage(self.driver)
        dashboard_page = login_page.do_successful_login_with(VALID_CREDENTIALS)
        self.assertEqual(dashboard_page.welcome_message(),
            fetch_(WELCOME_MESSAGE, from_(VALID_CREDENTIALS)))
        self.test_var = "help"
        self.driver.go_to(DATA_WINNER_SMS_TESTER_PAGE)
        sms_tester_page = SMSTesterPage(self.driver)
        sms_tester_page.send_sms_with(sms_data)
        self.assertEqual(sms_tester_page.get_response_message(), fetch_(MESSAGE, from_(sms_data)))
        return self

    @attr('functional_test', 'smoke')
    def test_verify_successful_sms_submission_log(self):
        """
        Function to test the successful SMS submission
        """
        self.prerequisites_of_sms_tester(VALID_DATA2)
        self.driver.go_to(DATA_WINNER_SUBMISSION_LOG_PAGE)
        time.sleep(3)
        submission_log_page = SubmissionLogPage(self.driver)
        self.assertRegexpMatches(submission_log_page.get_submission_message(SMS_DATA), fetch_(SMS_SUBMISSION, from_(SMS_DATA)))

    @attr('functional_test')
    def test_invalid_sms_submission_log(self):
        """
        Function to test the successful SMS submission
        """
        self.prerequisites_of_sms_tester(EXCEED_NAME_LENGTH2)
        self.driver.go_to(DATA_WINNER_SUBMISSION_LOG_PAGE)
        time.sleep(3)
        print self.test_var
        submission_log_page = SubmissionLogPage(self.driver)
        self.assertRegexpMatches(submission_log_page.get_submission_message(EXCEED_WORD_LIMIT), fetch_(SMS_SUBMISSION, from_(EXCEED_WORD_LIMIT)))
