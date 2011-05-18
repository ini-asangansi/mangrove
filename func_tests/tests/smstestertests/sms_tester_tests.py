# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from nose.plugins.attrib import attr
from nose.plugins.skip import SkipTest
from framework.base_test import BaseTest
from framework.utils.data_fetcher import fetch_, from_
from pages.smstesterpage.sms_tester_page import SMSTesterPage
from testdata.test_data import DATA_WINNER_SMS_TESTER_PAGE
from tests.smstestertests.sms_tester_data import *


class TestSMSTester(BaseTest):

    @attr('functional_test', 'smoke')
    def test_successful_sms_submission(self):
        """
        Function to test the successful SMS submission
        """
        self.driver.go_to(DATA_WINNER_SMS_TESTER_PAGE)
        sms_tester_page = SMSTesterPage(self.driver)
        sms_tester_page.send_sms_with(VALID_DATA)
        self.assertEqual(sms_tester_page.get_response_message(), fetch_(SUCCESS_MESSAGE, from_(VALID_DATA)))

    @attr('functional_test')
    def test_sms_player_without_entering_data(self):
        """
        Function to test the error message on the set up project page while
        creation of project
        """
        self.driver.go_to(DATA_WINNER_SMS_TESTER_PAGE)
        sms_tester_page = SMSTesterPage(self.driver)
        sms_tester_page.send_sms_with(BLANK_FIELDS)
        self.assertEqual(sms_tester_page.get_error_message(), fetch_(ERROR_MSG, from_(BLANK_FIELDS)))

    @attr('functional_test')
    def test_sms_player_for_exceeding_word_length(self):
        """
        Function to test the error message on the set up project page while
        creation of project
        """
        self.driver.go_to(DATA_WINNER_SMS_TESTER_PAGE)
        sms_tester_page = SMSTesterPage(self.driver)
        sms_tester_page.send_sms_with(EXCEED_NAME_LENGTH)
        self.assertEqual(sms_tester_page.get_response_message(), fetch_(ERROR_MSG, from_(EXCEED_NAME_LENGTH)))
