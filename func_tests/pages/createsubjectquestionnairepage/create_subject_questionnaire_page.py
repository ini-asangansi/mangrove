# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from framework.utils.common_utils import CommonUtilities, generateId
from pages.createquestionnairepage.create_questionnaire_page import CreateQuestionnairePage
from pages.page import Page
from framework.utils.data_fetcher import *
from pages.createsubjectquestionnairepage.create_subject_questionnaire_locator import *
from framework.utils.common_utils import *


class CreateSubjectQuestionnairePage(Page):

    def __init__(self, driver):
        Page.__init__(self, driver)

    def get_title(self):
        """
        Fetch the title of the web page

        Return title of the web page
        """
        page_title = self.driver.title
        return page_title

    def successfully_create_subject_questionnaire_with(self, subject_data):
        """
        Function to enter and save the data on set up project page

        Args:
        registration_data is data to fill in the different fields like first
        name, last name, telephone number and commune

        Return self
        """
        self.driver.find(SAVE_CHANGES_BTN).click()
        return CreateQuestionnairePage(self.driver)
