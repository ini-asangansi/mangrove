__author__ = 'kumarr'

from framework.mangrovetests.page import Page


class RegistrationConfirmationPage(Page):

    def __init__(self, driver):
        Page.__init__(self, driver)


    def registration_success_message(self):
        success_message = self.driver.find_element_by_css_selector("div[class^= 'success']").text
        print success_message
        return success_message




  