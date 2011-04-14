# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8



from framework.pages.page import Page
from framework.pages.registerconfirmationpage.registration_confirmation_locator import *


class RegistrationConfirmationPage(Page):

    def __init__(self, driver):
        Page.__init__(self, driver)


    def registration_success_message(self):
        success_message = self.driver.find(WELCOME_MESSAGE_LI).text
        return success_message




  