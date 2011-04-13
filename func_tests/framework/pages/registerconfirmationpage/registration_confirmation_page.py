# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

__author__ = 'kumarr'

from framework.pages.page import Page


class RegistrationConfirmationPage(Page):

    def __init__(self, driver):
        Page.__init__(self, driver)


    def registration_success_message(self):
        success_message = self.driver.find_element_by_css_selector("div[class^= 'form']").text
        return success_message




  