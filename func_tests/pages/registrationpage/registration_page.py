# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from framework.utils.common_utils import generateId

from pages.page import Page
from pages.registerconfirmationpage.registration_confirmation_page import RegistrationConfirmationPage
from framework.utils.data_fetcher import *
from pages.registrationpage.registration_locator import *
from tests.registrationtests.registration_data import *


class RegistrationPage(Page):

    def __init__(self, driver):
        Page.__init__(self, driver)

    def get_title(self):
        """Fetch the title of the web page

        Return title of the web page
        """
        page_title = self.driver.title
        return page_title

    def successful_registration_with(self, registration_data):
        self.driver.find_text_box(ORGANIZATION_NAME_TB).enter_text(
            fetch_(ORGANIZATION_NAME, from_(registration_data)))
        self.driver.find_text_box(ORGANIZATION_SECTOR_DD).enter_text(
            fetch_(ORGANIZATION_SECTOR, from_(registration_data)))
        self.driver.find_text_box(ORGANIZATION_ADDRESS_LINE1_TB).enter_text(
            fetch_(ORGANIZATION_ADDRESS_LINE1, from_(registration_data)))
        self.driver.find_text_box(ORGANIZATION_ADDRESS_LINE2_TB).enter_text(
            fetch_(ORGANIZATION_ADDRESS_LINE2, from_(registration_data)))
        self.driver.find_text_box(ORGANIZATION_CITY_TB).enter_text(
            fetch_(ORGANIZATION_CITY, from_(registration_data)))
        self.driver.find_text_box(ORGANIZATION_STATE_TB).enter_text(
            fetch_(ORGANIZATION_STATE, from_(registration_data)))
        self.driver.find_text_box(ORGANIZATION_COUNTRY_TB).enter_text(
            fetch_(ORGANIZATION_COUNTRY, from_(registration_data)))
        self.driver.find_text_box(ORGANIZATION_ZIPCODE_TB).enter_text(
            fetch_(ORGANIZATION_ZIPCODE, from_(registration_data)))
        self.driver.find_text_box(ORGANIZATION_OFFICE_PHONE_TB).enter_text(
            fetch_(ORGANIZATION_OFFICE_PHONE, from_(registration_data)))
        self.driver.find_text_box(ORGANIZATION_WEBSITE_TB).enter_text(
            fetch_(ORGANIZATION_WEBSITE, from_(registration_data)))
        self.driver.find_text_box(ORGANIZATION_TITLE_TB).enter_text(
            fetch_(TITLE, from_(registration_data)))
        self.driver.find_text_box(ORGANIZATION_FIRST_NAME_TB).enter_text(
            fetch_(FIRST_NAME, from_(registration_data)))
        self.driver.find_text_box(ORGANIZATION_LAST_NAME_TB).enter_text(
            fetch_(LAST_NAME, from_(registration_data)))
        email = fetch_(EMAIL, from_(registration_data)) + generateId() + "@ngo.com"
        self.driver.find_text_box(ORGANIZATION_EMAIL_TB).enter_text(email)
        self.driver.find_text_box(ORGANIZATION_PASSWORD_TB).enter_text(
            fetch_(REGISTRATION_PASSWORD, from_(registration_data)))
        self.driver.find_text_box(ORGANIZATION_CONFIRM_PASSWORD_TB).enter_text(
            fetch_(REGISTRATION_CONFIRM_PASSWORD, from_(registration_data)))
        self.driver.find(ORGANIZATION_REGISTER_BTN).click()
        return (RegistrationConfirmationPage(self.driver), email)

    def register_with(self, registration_data):
        self.driver.find_text_box(ORGANIZATION_NAME_TB).enter_text(
            fetch_(ORGANIZATION_NAME, from_(registration_data)))
        self.driver.find_text_box(ORGANIZATION_SECTOR_DD).enter_text(
            fetch_(ORGANIZATION_SECTOR, from_(registration_data)))
        self.driver.find_text_box(ORGANIZATION_ADDRESS_LINE1_TB).enter_text(
            fetch_(ORGANIZATION_ADDRESS_LINE1, from_(registration_data)))
        self.driver.find_text_box(ORGANIZATION_ADDRESS_LINE1_TB).enter_text(
            fetch_(ORGANIZATION_ADDRESS_LINE1, from_(registration_data)))
        self.driver.find_text_box(ORGANIZATION_CITY_TB).enter_text(
            fetch_(ORGANIZATION_CITY, from_(registration_data)))
        self.driver.find_text_box(ORGANIZATION_STATE_TB).enter_text(
            fetch_(ORGANIZATION_STATE, from_(registration_data)))
        self.driver.find_text_box(ORGANIZATION_COUNTRY_TB).enter_text(
            fetch_(ORGANIZATION_COUNTRY, from_(registration_data)))
        self.driver.find_text_box(ORGANIZATION_ZIPCODE_TB).enter_text(
            fetch_(ORGANIZATION_ZIPCODE, from_(registration_data)))
        self.driver.find_text_box(ORGANIZATION_OFFICE_PHONE_TB).enter_text(
            fetch_(ORGANIZATION_OFFICE_PHONE, from_(registration_data)))
        self.driver.find_text_box(ORGANIZATION_WEBSITE_TB).enter_text(
            fetch_(ORGANIZATION_WEBSITE, from_(registration_data)))
        self.driver.find_text_box(ORGANIZATION_TITLE_TB).enter_text(
            fetch_(TITLE, from_(registration_data)))
        self.driver.find_text_box(ORGANIZATION_FIRST_NAME_TB).enter_text(
            fetch_(FIRST_NAME, from_(registration_data)))
        self.driver.find_text_box(ORGANIZATION_LAST_NAME_TB).enter_text(
            fetch_(LAST_NAME, from_(registration_data)))
        self.driver.find_text_box(ORGANIZATION_EMAIL_TB).enter_text(
            fetch_(EMAIL, from_(registration_data)))
        self.driver.find_text_box(ORGANIZATION_PASSWORD_TB).enter_text(
            fetch_(REGISTRATION_PASSWORD, from_(registration_data)))
        self.driver.find_text_box(ORGANIZATION_CONFIRM_PASSWORD_TB).enter_text(
            fetch_(REGISTRATION_CONFIRM_PASSWORD, from_(registration_data)))
        self.driver.find(ORGANIZATION_REGISTER_BTN).click()
        return self

    def get_error_message(self):
        """
        Function to fetch the error messages from error label of the login
        page

        Return error message
        """
        error_message = ""
        locators = self.driver.find_elements_(ERROR_MESSAGE_LABEL)
        if locators:
            for locator in locators:
                error_message = error_message + locator.text
        return error_message.replace("\n", " ")
