# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from pages.dashboardpage.dashboard_locator import *
from pages.page import Page
from pages.registerreporterpage.register_reporter_page import ReporterRegistrationPage


class DashboardPage(Page):

    def __init__(self, driver):
        Page.__init__(self, driver)

    def welcome_message(self):
        """
        Function to fetch the Welcome message from the label provided on
        dashboard page.

        Return the Welcome message
         """
        welcome_message = self.driver.find(WELCOME_MESSAGE_LABEL).text
        return welcome_message

    def navigate_to_register_reporter_page(self):
        """
        Function to navigate to register a reporter page of the website.

        Return register reporter page
         """
        self.driver.find(REGISTER_REPORTER_LINK).click()
        return ReporterRegistrationPage(self.driver)
