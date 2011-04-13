# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from framework.pages.page import Page
from framework.pages.registerconfirmationpage.registration_confirmation_page import RegistrationConfirmationPage
from framework.utils.data_fetcher import *
from framework.pages.registrationpage.registration_locator import *
from tests.registrationtests.registration_data import *
from testdata.test_data import *


__author__ = 'kumarr'


class RegistrationPage(Page):

    def __init__(self, driver):
        Page.__init__(self, driver)

    def get_title(self):
        """Fetch the title of the web page

        Return title of the web page
        """
        page_title = self.driver.title
        return page_title

    def do_successful_registration(self, registration_data_for_successful_login ):
        self.driver.find_text_box(ORGANIZATION_NAME_TB).enter_text(fetch_(ORGANIZATION_NAME, from_(registration_data_for_successful_login)))
        self.driver.find_text_box(ORGANIZATION_SECTOR_DD).enter_text(fetch_(ORGANIZATION_SECTOR, from_(registration_data_for_successful_login)))
        self.driver.find_text_box(ORGANIZATION_ADDRESS_LINE1_TB).enter_text(fetch_(ORGANIZATION_ADDRESS_LINE1, from_(registration_data_for_successful_login)))
        self.driver.find_text_box(ORGANIZATION_ADDRESS_LINE1_TB).enter_text(fetch_(ORGANIZATION_ADDRESS_LINE1, from_(registration_data_for_successful_login)))
        self.driver.find_text_box(ORGANIZATION_CITY_TB).enter_text(fetch_(ORGANIZATION_CITY, from_(registration_data_for_successful_login)))
        self.driver.find_text_box(ORGANIZATION_STATE_TB).enter_text(fetch_(ORGANIZATION_STATE, from_(registration_data_for_successful_login)))
        self.driver.find_text_box(ORGANIZATION_COUNTRY_TB).enter_text(fetch_(ORGANIZATION_COUNTRY,from_(registration_data_for_successful_login)))
        self.driver.find_text_box(ORGANIZATION_ZIPCODE_TB).enter_text(fetch_(ORGANIZATION_ZIPCODE,from_(registration_data_for_successful_login)))
        self.driver.find_text_box(ORGANIZATION_OFFICE_PHONE_TB).enter_text(fetch_(ORGANIZATION_OFFICE_PHONE,from_(registration_data_for_successful_login)))
        self.driver.find_text_box(ORGANIZATION_WEBSITE_TB).enter_text(fetch_(ORGANIZATION_WEBSITE,from_(registration_data_for_successful_login)))
        self.driver.find_text_box(ORGANIZATION_TITLE_TB).enter_text(fetch_(TITLE,from_(registration_data_for_successful_login)))
        self.driver.find_text_box(ORGANIZATION_FIRST_NAME_TB).enter_text(fetch_(FIRST_NAME,from_(registration_data_for_successful_login)))
        self.driver.find_text_box(ORGANIZATION_LAST_NAME_TB).enter_text(fetch_(LAST_NAME,from_(registration_data_for_successful_login)))
        self.driver.find_text_box(ORGANIZATION_EMAIL_TB).enter_text(fetch_(EMAIL,from_(registration_data_for_successful_login)))
        self.driver.find_text_box(ORGANIZATION_PASSWORD_TB).enter_text(fetch_(REGISTRATION_PASSWORD,from_(registration_data_for_successful_login)))
        self.driver.find_text_box(ORGANIZATION_CONFIRM_PASSWORD_TB).enter_text(fetch_(REGISTRATION_CONFIRM_PASSWORD,from_(registration_data_for_successful_login)))
        self.driver.find(ORGANIZATION_REGISTER_B).click()
        return RegistrationConfirmationPage(self.driver)


    def enter_existing_email_id_and_click_register(self, registration_data_for_existing_email_error):
        self.driver.find_text_box(ORGANIZATION_NAME_TB).enter_text(fetch_(ORGANIZATION_NAME,from_(registration_data_for_existing_email_error)))
        self.driver.find_text_box(ORGANIZATION_SECTOR_DD).enter_text(fetch_(ORGANIZATION_SECTOR,from_(registration_data_for_existing_email_error)))
        self.driver.find_text_box(ORGANIZATION_ADDRESS_LINE1_TB).enter_text(fetch_(ORGANIZATION_ADDRESS_LINE1,from_(registration_data_for_existing_email_error)))
        self.driver.find_text_box(ORGANIZATION_ADDRESS_LINE1_TB).enter_text(fetch_(ORGANIZATION_ADDRESS_LINE1,from_(registration_data_for_existing_email_error)))
        self.driver.find_text_box(ORGANIZATION_CITY_TB).enter_text(fetch_(ORGANIZATION_CITY,from_(registration_data_for_existing_email_error)))
        self.driver.find_text_box(ORGANIZATION_STATE_TB).enter_text(fetch_(ORGANIZATION_STATE,from_(registration_data_for_existing_email_error)))
        self.driver.find_text_box(ORGANIZATION_COUNTRY_TB).enter_text(fetch_(ORGANIZATION_COUNTRY,from_(registration_data_for_existing_email_error)))
        self.driver.find_text_box(ORGANIZATION_ZIPCODE_TB).enter_text(fetch_(ORGANIZATION_ZIPCODE,from_(registration_data_for_existing_email_error)))
        self.driver.find_text_box(ORGANIZATION_OFFICE_PHONE_TB).enter_text(fetch_(ORGANIZATION_OFFICE_PHONE,from_(registration_data_for_existing_email_error)))
        self.driver.find_text_box(ORGANIZATION_WEBSITE_TB).enter_text(fetch_(ORGANIZATION_WEBSITE,from_(registration_data_for_existing_email_error)))
        self.driver.find_text_box(ORGANIZATION_TITLE_TB).enter_text(fetch_(TITLE,from_(registration_data_for_existing_email_error)))
        self.driver.find_text_box(ORGANIZATION_FIRST_NAME_TB).enter_text(fetch_(FIRST_NAME,from_(registration_data_for_existing_email_error)))
        self.driver.find_text_box(ORGANIZATION_LAST_NAME_TB).enter_text(fetch_(LAST_NAME,from_(registration_data_for_existing_email_error)))
        self.driver.find_text_box(ORGANIZATION_EMAIL_TB).enter_text(fetch_(EMAIL,from_(registration_data_for_existing_email_error)))
        self.driver.find_text_box(ORGANIZATION_PASSWORD_TB).enter_text(fetch_(REGISTRATION_PASSWORD,from_(registration_data_for_existing_email_error)))
        self.driver.find_text_box(ORGANIZATION_CONFIRM_PASSWORD_TB).enter_text(fetch_(REGISTRATION_CONFIRM_PASSWORD,from_(registration_data_for_existing_email_error)))
        self.driver.find(ORGANIZATION_REGISTER_B).click()
        return RegistrationPage(self.driver)

    def existing_email_error_message(self):
        existing_email_error_message = self.driver.find_element_by_css_selector(".errorlist li").text
        print existing_email_error_message
        return existing_email_error_message