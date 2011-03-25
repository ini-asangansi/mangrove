from framework.openMangrove.Page import Page

__author__ = 'kumarr'


class DashboardPage(Page):

    def __init__(self, driver):
        Page.__init__(self, driver)

    def WelcomeMessage(self):

        welcomeMessage = self.driver.find_element_by_css_selector(".span-9 h4").text
        return welcomeMessage
