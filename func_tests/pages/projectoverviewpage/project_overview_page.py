# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from pages.createprojectpage.create_project_page import CreateProjectPage
from pages.datapage.data_page import DataPage
from pages.projectoverviewpage.project_overview_locator import *
from pages.page import Page
from pages.submissionlogpage.submission_log_page import SubmissionLogPage


class ProjectOverviewPage(Page):

    def __init__(self, driver):
        Page.__init__(self, driver)

    def navigate_to_data_page(self):
        """
        Function to navigate data page

        Return data page
         """
        self.driver.find(DATA_TAB).click()
        return DataPage(self.driver)

    def navigate_to_create_project_page(self):
        """
        Function to navigate to create project page

        Return create project page
         """
        self.driver.find(PROJECT_EDIT_LINK).click()
        return CreateProjectPage(self.driver)
