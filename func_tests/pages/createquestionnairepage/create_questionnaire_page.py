# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from framework.utils.common_utils import CommonUtilities

from pages.page import Page
from framework.utils.data_fetcher import *
from pages.createquestionnairepage.create_questionnaire_locator import *
from tests.createquestionnairetests.create_questionnaire_data import *


class CreateQuestionnairePage(Page):

    def __init__(self, driver):
        Page.__init__(self, driver)

    def get_title(self):
        """
        Fetch the title of the web page

        Return title of the web page
        """
        page_title = self.driver.title
        return page_title

    def successfully_create_questionnaire_with(self, questionnaire_data):
        """
        Function to enter and save the data on set up project page

        Args:
        registration_data is data to fill in the different fields like first
        name, last name, telephone number and commune

        Return self
        """
        self.driver.find_text_box(QUESTIONNAIRE_CODE_TB).enter_text(
            fetch_(QUESTIONNAIRE_CODE, from_(questionnaire_data)))
        self.driver.find(ADD_QUESTION_LINK).click()

        '''self.driver.find_text_box(PROJECT_BACKGROUND_TB).enter_text(
            fetch_(PROJECT_BACKGROUND, from_(questionnaire_data)))
        # Selecting radio button according to given option
        project_type = fetch_(PROJECT_TYPE, from_(questionnaire_data))
        if project_type == "survey":
            self.driver.find(SURVEY_PROJECT_RB).toggle()
        elif project_type == "public information":
            self.driver.find(PUBLIC_INFORMATION_RB).toggle()
        # Selecting check box according to given options
        devices = fetch_(DEVICES, from_(project_data)).split(",")
        if "sms" in devices:
            self.driver.find(SMS_CB).toggle()
        if "smartphone" in devices:
            self.driver.find(SMART_PHONE_CB).toggle()
        if "web" in devices:
            self.driver.find(WEB_CB).toggle()
        self.driver.find(SAVE_CHANGES_BTN).click()
        return self

    def create_questionnaire_with(self, project_data):
        """
        Function to enter and save the data on set up project page

        Args:
        registration_data is data to fill in the different fields like first
        name, last name, telephone number and commune

        Return self
        """
        self.driver.find_text_box(QUESTIONNAIRE_CODE_TB).enter_text(
            fetch_(PROJECT_NAME, from_(project_data)))
        self.driver.find_text_box(PROJECT_BACKGROUND_TB).enter_text(
            fetch_(PROJECT_BACKGROUND, from_(project_data)))
        # Selecting radio button according to given option
        project_type = fetch_(PROJECT_TYPE, from_(project_data))
        if project_type == "survey":
            self.driver.find(SURVEY_PROJECT_RB).toggle()
        elif project_type == "public information":
            self.driver.find(PUBLIC_INFORMATION_RB).toggle()
        # Selecting check box according to given options
        devices = fetch_(DEVICES, from_(project_data))
        if devices == "sms":
            self.driver.find(SMS_CB).toggle()
        elif devices == "smartphone":
            self.driver.find(SMART_PHONE_CB).toggle()
        elif devices == "web":
            self.driver.find(WEB_CB).toggle()
        self.driver.find(SAVE_CHANGES_BTN).click()'''
        return self

    def get_error_message(self):
        """
        Function to fetch the error messages from error label of the register
        reporter page

        Return error message
        """
        error_message = ""
        comm_utils = CommonUtilities(self.driver)
        locator = comm_utils.is_element_present(PROJECT_NAME_ERROR_MSG_LABEL)
        if locator:
            error_message = error_message + "Name  " + locator.text
        locator = comm_utils.is_element_present(PROJECT_TYPE_ERROR_MSG_LABEL)
        if locator:
            error_message = error_message + "Project Type  " + locator.text
        return error_message == "" and "No error message on the page" or error_message
