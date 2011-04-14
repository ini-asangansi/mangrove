# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from framework.pages.page import Page
from framework.pages.registerconfirmationpage.registration_confirmation_page import RegistrationConfirmationPage
from framework.utils.common_utils import CommonUtilities
from framework.pages.registrationpage.registration_locator import *
from framework.utils.data_fetcher import *
from testdata.test_data import *





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
        self.driver.find_text_box(ORGANIZATION_NAME_TB[LOCATOR]).enter_text(put(ORGANIZATION_NAME,of(registration_data_for_successful_login)))
        self.driver.find_text_box(ORGANIZATION_SECTOR_DD[LOCATOR]).enter_text(put(ORGANIZATION_SECTOR,of(registration_data_for_successful_login)))
        self.driver.find_text_box(ORGANIZATION_ADDRESS_LINE1_TB[LOCATOR]).enter_text(put(ORGANIZATION_ADDRESS_LINE1,of(registration_data_for_successful_login)))
        self.driver.find_text_box(ORGANIZATION_ADDRESS_LINE1_TB[LOCATOR]).enter_text(put(ORGANIZATION_ADDRESS_LINE1,of(registration_data_for_successful_login)))
        self.driver.find_text_box(ORGANIZATION_CITY_TB[LOCATOR]).enter_text(put(ORGANIZATION_CITY,of(registration_data_for_successful_login)))
        self.driver.find_text_box(ORGANIZATION_STATE_TB[LOCATOR]).enter_text(put(ORGANIZATION_STATE,of(registration_data_for_successful_login)))
        self.driver.find_text_box(ORGANIZATION_COUNTRY_TB[LOCATOR]).enter_text(put(ORGANIZATION_COUNTRY,of(registration_data_for_successful_login)))
        self.driver.find_text_box(ORGANIZATION_ZIPCODE_TB[LOCATOR]).enter_text(put(ORGANIZATION_ZIPCODE,of(registration_data_for_successful_login)))
        self.driver.find_text_box(ORGANIZATION_OFFICE_PHONE_TB[LOCATOR]).enter_text(put(ORGANIZATION_OFFICE_PHONE,of(registration_data_for_successful_login)))
        self.driver.find_text_box(ORGANIZATION_WEBSITE_TB[LOCATOR]).enter_text(put(ORGANIZATION_WEBSITE,of(registration_data_for_successful_login)))
        self.driver.find_text_box(ORGANIZATION_TITLE_TB[LOCATOR]).enter_text(put(TITLE,of(registration_data_for_successful_login)))
        self.driver.find_text_box(ORGANIZATION_FIRST_NAME_TB[LOCATOR]).enter_text(put(FIRST_NAME,of(registration_data_for_successful_login)))
        self.driver.find_text_box(ORGANIZATION_LAST_NAME_TB[LOCATOR]).enter_text(put(LAST_NAME,of(registration_data_for_successful_login)))
        self.driver.find_text_box(ORGANIZATION_EMAIL_TB[LOCATOR]).enter_text(put(EMAIL,of(registration_data_for_successful_login)))
        self.driver.find_text_box(ORGANIZATION_PASSWORD_TB[LOCATOR]).enter_text(put(REGISTRATION_PASSWORD,of(registration_data_for_successful_login)))
        self.driver.find_text_box(ORGANIZATION_CONFIRM_PASSWORD_TB[LOCATOR]).enter_text(put(REGISTRATION_CONFIRM_PASSWORD,of(registration_data_for_successful_login)))
        self.driver.find_button(ORGANIZATION_REGISTER_B[LOCATOR]).click()
        return RegistrationConfirmationPage(self.driver)


    def enter_existing_email_id_and_click_register(self, registration_data_for_existing_email_error):
        self.driver.find_text_box(ORGANIZATION_NAME_TB[LOCATOR]).enter_text(put(ORGANIZATION_NAME,of(registration_data_for_existing_email_error)))
        self.driver.find_text_box(ORGANIZATION_SECTOR_DD[LOCATOR]).enter_text(put(ORGANIZATION_SECTOR,of(registration_data_for_existing_email_error)))
        self.driver.find_text_box(ORGANIZATION_ADDRESS_LINE1_TB[LOCATOR]).enter_text(put(ORGANIZATION_ADDRESS_LINE1,of(registration_data_for_existing_email_error)))
        self.driver.find_text_box(ORGANIZATION_ADDRESS_LINE1_TB[LOCATOR]).enter_text(put(ORGANIZATION_ADDRESS_LINE1,of(registration_data_for_existing_email_error)))
        self.driver.find_text_box(ORGANIZATION_CITY_TB[LOCATOR]).enter_text(put(ORGANIZATION_CITY,of(registration_data_for_existing_email_error)))
        self.driver.find_text_box(ORGANIZATION_STATE_TB[LOCATOR]).enter_text(put(ORGANIZATION_STATE,of(registration_data_for_existing_email_error)))
        self.driver.find_text_box(ORGANIZATION_COUNTRY_TB[LOCATOR]).enter_text(put(ORGANIZATION_COUNTRY,of(registration_data_for_existing_email_error)))
        self.driver.find_text_box(ORGANIZATION_ZIPCODE_TB[LOCATOR]).enter_text(put(ORGANIZATION_ZIPCODE,of(registration_data_for_existing_email_error)))
        self.driver.find_text_box(ORGANIZATION_OFFICE_PHONE_TB[LOCATOR]).enter_text(put(ORGANIZATION_OFFICE_PHONE,of(registration_data_for_existing_email_error)))
        self.driver.find_text_box(ORGANIZATION_WEBSITE_TB[LOCATOR]).enter_text(put(ORGANIZATION_WEBSITE,of(registration_data_for_existing_email_error)))
        self.driver.find_text_box(ORGANIZATION_TITLE_TB[LOCATOR]).enter_text(put(TITLE,of(registration_data_for_existing_email_error)))
        self.driver.find_text_box(ORGANIZATION_FIRST_NAME_TB[LOCATOR]).enter_text(put(FIRST_NAME,of(registration_data_for_existing_email_error)))
        self.driver.find_text_box(ORGANIZATION_LAST_NAME_TB[LOCATOR]).enter_text(put(LAST_NAME,of(registration_data_for_existing_email_error)))
        self.driver.find_text_box(ORGANIZATION_EMAIL_TB[LOCATOR]).enter_text(put(EMAIL,of(registration_data_for_existing_email_error)))
        self.driver.find_text_box(ORGANIZATION_PASSWORD_TB[LOCATOR]).enter_text(put(REGISTRATION_PASSWORD,of(registration_data_for_existing_email_error)))
        self.driver.find_text_box(ORGANIZATION_CONFIRM_PASSWORD_TB[LOCATOR]).enter_text(put(REGISTRATION_CONFIRM_PASSWORD,of(registration_data_for_existing_email_error)))
        self.driver.find_button(ORGANIZATION_REGISTER_B[LOCATOR]).click()
        return RegistrationPage(self.driver)

    def existing_email_error_message(self):
        existing_email_error_message = self.driver.find_element_by_css_selector(".errorlist li").text
        print existing_email_error_message
        return existing_email_error_message