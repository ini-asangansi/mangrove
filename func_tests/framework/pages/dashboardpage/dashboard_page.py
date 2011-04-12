# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from framework.pages.page import Page

__author__ = 'kumarr'


class DashboardPage(Page):

    def __init__(self, driver):
        Page.__init__(self, driver)

    def welcome_message(self):
        """ Function to fetch the Welcome message from the label provided on
        dashboard page.

        Return the Welcome message
         """
        welcome_message = self.driver.find_element_by_css_selector(".span-9 h4").text
        return welcome_message

    