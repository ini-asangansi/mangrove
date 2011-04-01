from framework.mangrovetests.page import Page

__author__ = 'kumarr'


class RegistrationPage(Page):

    def __init__(self, driver):
        Page.__init__(self, driver)

    def GetTitle(self):
        pageTitle = self.driver.title
        return pageTitle