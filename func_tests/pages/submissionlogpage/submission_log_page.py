# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from framework.utils.common_utils import CommonUtilities
from pages.smstesterpage.sms_tester_locator import *
from pages.page import Page
from framework.utils.data_fetcher import *
from tests.smstestertests.sms_tester_data import *
from framework.utils.common_utils import *


class SubmissionLogPage(Page):

    def __init__(self, driver):
        Page.__init__(self, driver)

    def get_title(self):
        """
        Fetch the title of the web page

        Return title of the web page
        """
        page_title = self.driver.title()
        return page_title

    def get_submission_message(self):
        """
        Function to fetch the submission log from the row of the table

        Return submission log
        """
        return self.driver.find(SUBMISSION_LOG_TR).text