# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from nose.plugins.attrib import attr
from nose.plugins.skip import SkipTest
from framework.base_test import BaseTest
from framework.utils.data_fetcher import fetch_, from_
from pages.smstesterpage.sms_tester_page import SMSTesterPage
from pages.submissionlogpage.submission_log_page import SubmissionLogPage
from testdata.test_data import DATA_WINNER_SUBMISSION_LOG_PAGE, DATA_WINNER_SMS_TESTER_PAGE
from tests.smstestertests.sms_tester_data import VALID_DATA, SUCCESS_MESSAGE
from tests.submissionlogtests.submission_log_data import *


class TestSubmissionLog(BaseTest):

    def prerequisites_of_create_questionnaire(self):
        self.driver.go_to(DATA_WINNER_SMS_TESTER_PAGE)
        sms_tester_page = SMSTesterPage(self.driver)
        sms_tester_page.send_sms_with(VALID_DATA)
        self.assertEqual(sms_tester_page.get_response_message(), fetch_(SUCCESS_MESSAGE, from_(VALID_DATA)))
        return self

    @SkipTest
    @attr('functional_test')
    def test_verify_successful_sms_submission_log(self):
        """
        Function to test the successful SMS submission
        """
        self.driver.go_to(DATA_WINNER_SUBMISSION_LOG_PAGE)
        submission_log_page = SubmissionLogPage(self.driver)
        self.assertRegexpMatches(submission_log_page.get_submission_message(), fetch_(SMS_SUBMISSION, from_(SMS_DATA)))