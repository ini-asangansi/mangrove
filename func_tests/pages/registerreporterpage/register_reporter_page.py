# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from pages.page import Page
from framework.utils.data_fetcher import *
from pages.registerreporterpage.register_reporter_locator import *
from tests.registerreportertests.register_reporter_data import *


class ReporterRegistrationPage(Page):

    def __init__(self, driver):
        Page.__init__(self, driver)

    def get_title(self):
        """
        Fetch the title of the web page

        Return title of the web page
        """
        page_title = self.driver.title
        return page_title

    def register_with(self, registration_data):
        """
        Function to enter and submit the data on register reporter page

        Args:
        registration_data is data to fill in the different fields like first
        name, last name, telephone number and commune

        Return self
        """
        self.driver.find_text_box(FIRST_NAME_TB).enter_text(
            fetch_(NAME, from_(registration_data)))
        self.driver.find_text_box(TELEPHONE_NUMBER_TB).enter_text(
            fetch_(TELEPHONE_NUMBER, from_(registration_data)))
        self.driver.find_text_box(COMMUNE_TB).enter_text(
            fetch_(COMMUNE, from_(registration_data)))
        self.driver.find_text_box(GPS_TB).enter_text(
            fetch_(GPS, from_(registration_data)))
        self.driver.find(REGISTER_BTN).click()
        return self

    def get_error_message(self):
        """
        Function to fetch the error messages from error label of the register
         reporter page

        Return error message
        """
        error_message = ""
        locators = self.driver.find_elements_(ERROR_MESSAGE_LABEL)
        if locators:
            for locator in locators:
                error_message = error_message + locator.text
        return error_message.replace("\n", " ")

    def get_success_message(self):
        """
        Function to fetch the success message from flash label of the register
         reporter page

        Return success message
        """
        error_message = ""
        locator = self.driver.find(FLASH_MESSAGE_LABEL)
        return locator.text
