__author__ = 'kumarr'

from framework.mangrovetests.page import Page


class RegistrationConfirmationPage(Page):

    def __init__(self, driver):
        Page.__init__(self, driver)


    def organization_name(self):
        organization_name = self.driver.find_element_by_css_selector(".span-9 h4").text
        pass




  