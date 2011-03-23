from framework.openMangrove.Page import Page

__author__ = 'kumarr'

class DashboardPage(Page):

    def __init__(self, driver):
        Page.__init__(self, driver)

    def LoginSuccessfulMessage(self):
        messageOnPage = self.driver.get_body_text()
        return messageOnPage

