# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from framework.utils.common_utils import generateId, CommonUtilities

from pages.page import Page
from framework.utils.data_fetcher import *
from pages.registersubjectpage.register_subject_locator import *
from tests.registersubjecttests.register_subject_data import *


class RegisterSubjectPage(Page):

    def __init__(self, driver):
        Page.__init__(self, driver)

    def get_title(self):
        """
        Fetch the title of the web page

        Return title of the web page
        """
        page_title = self.driver.title
        return page_title

    def successfully_register_subject_with(self, registration_data):
        """
        Function to fill data with random short name and submit on register a subject page

        Args:
        registration_data is data to fill in the different fields like short name, location, Geo Code,
        description and mobile number

        Return flash message
        """
        entity_type = fetch_(ENTITY_TYPE, from_(registration_data))
        self.driver.execute_script("document.getElementById('id_entity_type').value = '" + entity_type + "';")
        self.driver.find_drop_down(ENTITY_TYPE_DD).set_selected(entity_type)
#        self.driver.find_drop_down(ENTITY_TYPE_DD).set_selected(
#            DROP_DOWN_OPTION_CSS % entity_type)
        short_name = fetch_(SHORT_NAME, from_(registration_data))
        if not fetch_(AUTO_GENERATE, from_(registration_data)):
            self.driver.find(AUTO_GENERATE_CB).click()
            short_name = short_name + generateId()
            self.driver.find_text_box(SHORT_NAME_ENABLED_TB).enter_text()
        self.driver.find_text_box(NAME_TB).enter_text(
            fetch_(NAME, from_(registration_data)))
        self.driver.find_text_box(LOCATION_TB).enter_text(
            fetch_(LOCATION, from_(registration_data)))
        self.driver.find_text_box(GEO_CODE_TB).enter_text(
            fetch_(GEO_CODE, from_(registration_data)))
        self.driver.find_text_box(DESCRIPTION_TB).enter_text(
            fetch_(DESCRIPTION, from_(registration_data)))
        self.driver.find_text_box(MOBILE_NUMBER_TB).enter_text(
            fetch_(MOBILE_NUMBER, from_(registration_data)))
        self.driver.find(REGISTER_BTN).click()
        return fetch_(SUCCESS_MSG, from_(registration_data)) + short_name

    def register_subject_with(self, registration_data):
        """
        Function to fill and submit data on register a subject page

        Args:
        registration_data is data to fill in the different fields like short name, location, Geo Code,
        description and mobile number

        Return self
        """
        entity_type = fetch_(ENTITY_TYPE, from_(registration_data))
        self.driver.find_drop_down(ENTITY_TYPE_DD).click()
        self.driver.find(by_css(DROP_DOWN_OPTION_CSS % entity_type)).click()
        short_name = fetch_(SHORT_NAME, from_(registration_data))
        if not fetch_(AUTO_GENERATE, from_(registration_data)):
            self.driver.find(AUTO_GENERATE_CB).click()
            self.driver.find_text_box(SHORT_NAME_ENABLED_TB).enter_text()
        self.driver.find_text_box(NAME_TB).enter_text(
            fetch_(NAME, from_(registration_data)))
        self.driver.find_text_box(LOCATION_TB).enter_text(
            fetch_(LOCATION, from_(registration_data)))
        self.driver.find_text_box(GEO_CODE_TB).enter_text(
            fetch_(GEO_CODE, from_(registration_data)))
        self.driver.find_text_box(DESCRIPTION_TB).enter_text(
            fetch_(DESCRIPTION, from_(registration_data)))
        self.driver.find_text_box(MOBILE_NUMBER_TB).enter_text(
            fetch_(MOBILE_NUMBER, from_(registration_data)))
        self.driver.find(REGISTER_BTN).click()
        return self

    def get_error_message(self):
        """
        Function to fetch the error messages from error label of the register
         subject page

        Return error message
        """
        error_message = ""
        locators = self.driver.find_elements_(ERROR_MESSAGE_LABEL)
        if locators:
            for locator in locators:
                error_message = error_message + locator.text
        return error_message.replace("\n", " ")

    def get_flash_message(self):
        """
        Function to fetch the flash message from flash label of the register
         subject page

        Return message
        """
        comm_utils = CommonUtilities(self.driver)
        comm_utils.wait_for_element(5, FLASH_MESSAGE_LABEL)
        return self.driver.find(FLASH_MESSAGE_LABEL).text
