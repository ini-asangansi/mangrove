# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from framework.utils.common_utils import CommonUtilities, generateId
from pages.createsubjectquestionnairepage.create_subject_questionnaire_page import CreateSubjectQuestionnairePage
from pages.page import Page
from framework.utils.data_fetcher import *
from pages.createprojectpage.create_project_locator import *
from tests.createprojecttests.create_project_data import *
from framework.utils.common_utils import *


class CreateProjectPage(Page):

    def __init__(self, driver):
        Page.__init__(self, driver)

    def get_title(self):
        """
        Fetch the title of the web page

        Return title of the web page
        """
        page_title = self.driver.title
        return page_title

    def successfully_create_project_with(self, project_data):
        """
        Function to enter and save the data on set up project page

        Args:
        registration_data is data to fill in the different fields like first
        name, last name, telephone number and commune

        Return self
        """
        project_name = fetch_(PROJECT_NAME, from_(project_data))
        gen_ramdom = fetch_(GEN_RANDOM, from_(project_data))
        if gen_ramdom:
            project_name = project_name + generateId()
        self.driver.find_text_box(PROJECT_NAME_TB).enter_text(project_name)
        self.driver.find_text_box(PROJECT_BACKGROUND_TB).enter_text(
            fetch_(PROJECT_BACKGROUND, from_(project_data)))
        # Selecting radio button according to given option
        project_type = fetch_(PROJECT_TYPE, from_(project_data))
        if project_type == "survey":
            self.driver.find(SURVEY_PROJECT_RB).click()
        elif project_type == "public information":
            self.driver.find(PUBLIC_INFORMATION_RB).click()
        subject = fetch_(SUBJECT, from_(project_data))
        if len(subject) != 0:
            self.driver.execute_script("document.getElementById('id_entity_type').value = '" + subject + "';")
        # Selecting check box according to given options
        devices = fetch_(DEVICES, from_(project_data)).split(",")
        comm_utils = CommonUtilities(self.driver)
        # Selecting and Deselecting SMS checkbox for devices as per given option
        if "sms" in devices:
            if not(comm_utils.is_element_present(SMS_CB_CHECKED)):
                self.driver.find(SMS_CB).toggle()
        elif comm_utils.is_element_present(SMS_CB_CHECKED):
                self.driver.find(SMS_CB).toggle()
        # Selecting and Deselecting Smart phone checkbox for devices as per
        # given option
        if "smartphone" in devices:
            if not(comm_utils.is_element_present(SMART_PHONE_CB_CHECKED)):
                self.driver.find(SMART_PHONE_CB).toggle()
        elif comm_utils.is_element_present(SMART_PHONE_CB_CHECKED):
                self.driver.find(SMART_PHONE_CB).toggle()
        #Selecting and Deselecting Web checkbox for devices as per given option
        if "web" in devices:
            if not(comm_utils.is_element_present(WEB_CB_CHECKED)):
                self.driver.find(WEB_CB).toggle()
        elif comm_utils.is_element_present(WEB_CB_CHECKED):
                self.driver.find(WEB_CB).toggle()
        self.driver.find(SAVE_CHANGES_BTN).click()
        return CreateSubjectQuestionnairePage(self.driver)

    def create_project_with(self, project_data):
        """
        Function to enter and save the data on set up project page

        Args:
        registration_data is data to fill in the different fields like first
        name, last name, telephone number and commune

        Return self
        """
        self.driver.find_text_box(PROJECT_NAME_TB).enter_text(
            fetch_(PROJECT_NAME, from_(project_data)))
        self.driver.find_text_box(PROJECT_BACKGROUND_TB).enter_text(
            fetch_(PROJECT_BACKGROUND, from_(project_data)))
        # Selecting radio button according to given option
        project_type = fetch_(PROJECT_TYPE, from_(project_data))
        if project_type == "survey":
            self.driver.find(SURVEY_PROJECT_RB).click()
        elif project_type == "public information":
            self.driver.find(PUBLIC_INFORMATION_RB).click()
        # Selecting check box according to given options
        devices = fetch_(DEVICES, from_(project_data)).split(",")
        comm_utils = CommonUtilities(self.driver)
        # Selecting and Deselecting SMS checkbox for devices as per given option
        if "sms" in devices:
            if not(comm_utils.is_element_present(SMS_CB_CHECKED)):
                self.driver.find(SMS_CB).toggle()
        elif comm_utils.is_element_present(SMS_CB_CHECKED):
                self.driver.find(SMS_CB).toggle()
        # Selecting and Deselecting Smart phone checkbox for devices as per
        # given option
        if "smartphone" in devices:
            if not(comm_utils.is_element_present(SMART_PHONE_CB_CHECKED)):
                self.driver.find(SMART_PHONE_CB).toggle()
        elif comm_utils.is_element_present(SMART_PHONE_CB_CHECKED):
                self.driver.find(SMART_PHONE_CB).toggle()
        #Selecting and Deselecting Web checkbox for devices as per given option
        if "web" in devices:
            if not(comm_utils.is_element_present(WEB_CB_CHECKED)):
                self.driver.find(WEB_CB).toggle()
        elif comm_utils.is_element_present(WEB_CB_CHECKED):
                self.driver.find(WEB_CB).toggle()
        self.driver.find(SAVE_CHANGES_BTN).click()
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
