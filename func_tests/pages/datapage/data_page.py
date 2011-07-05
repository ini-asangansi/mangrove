# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from pages.datapage.data_locator import *
from pages.page import Page
from pages.submissionlogpage.submission_log_page import SubmissionLogPage


class DataPage(Page):

    def __init__(self, driver):
        Page.__init__(self, driver)

    def navigate_to_all_data_record_page(self):
        """
        Function to navigate all data record page

        Return data all data record
         """
        self.driver.find(ALL_DATA_RECORDS_LINK).click()
        return SubmissionLogPage(self.driver)
