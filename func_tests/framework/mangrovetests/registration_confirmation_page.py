from resources.element_locators import ORGANIZATION_NAME_TB

__author__ = 'kumarr'

from framework.mangrovetests.page import Page


class RegistrationConfirmationPage(Page):

    def __init__(self, driver):
        Page.__init__(self, driver)


    def registration_success_message(self):
        success_message = self.driver.find_element_by_css_selector("div[class^= 'success']").text
        return success_message




  