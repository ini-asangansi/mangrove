# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from pages.createprojectpage.create_project_page import CreateProjectPage
from pages.projectoverviewpage.project_overview_locator import VIEW_SUBMISSIONS_CLICK_HERE_LINK
from pages.page import Page
from pages.submissionlogpage.submission_log_page import SubmissionLogPage


class ProjectOverviewPage(Page):

    def __init__(self, driver):
        Page.__init__(self, driver)

    def navigate_to_submission_log_page(self):
        """
        Function to navigate to submission log page

        Return submission log page
         """
        self.driver.find(VIEW_SUBMISSIONS_CLICK_HERE_LINK).click()
        return SubmissionLogPage(self.driver)
