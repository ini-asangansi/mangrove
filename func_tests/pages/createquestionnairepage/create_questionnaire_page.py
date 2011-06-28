# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from time import time
from framework.utils.common_utils import CommonUtilities, generateId

from pages.page import Page
from framework.utils.data_fetcher import *
from pages.createquestionnairepage.create_questionnaire_locator import *
from tests.createquestionnairetests.create_questionnaire_data import *
from framework.utils.common_utils import *
import time


class CreateQuestionnairePage(Page):

    def __init__(self, driver):
        Page.__init__(self, driver)
        self.SELECT_FUNC = {WORD: self.configure_word_type_question,
                   NUMBER: self.configure_number_type_question,
                   DATE: self.configure_date_type_question,
                   LIST_OF_CHOICES: self.configure_list_of_choices_type_question,
                   GEO: self.configure_geo_type_question}

    def get_title(self):
        """
        Fetch the title of the web page

        Return title of the web page
        """
        page_title = self.driver.title
        return page_title

    def create_questionnaire_with(self, questionnaire_data):
        """
        Function to create a questionnaire on the 'create questionnaire' page

        Args:
        questionnaire_data is data to fill in the different fields of the questionnaire page

        Return self
        """
        questionnaire_code = fetch_(QUESTIONNAIRE_CODE, from_(questionnaire_data))
        gen_ramdom = fetch_(GEN_RANDOM, from_(questionnaire_data))
        if gen_ramdom:
            questionnaire_code = questionnaire_code + generateId()
        self.driver.find_text_box(QUESTIONNAIRE_CODE_TB).enter_text(questionnaire_code)
        self.create_default_question(questionnaire_data[DEFAULT_QUESTION], DEFAULT_QUESTION_LINK)
        for question in fetch_(QUESTIONS, from_(questionnaire_data)):
            self.driver.find(ADD_A_QUESTION_LINK).click()
            self.fill_question_and_code_tb(question)
            self.SELECT_FUNC[fetch_(TYPE, from_(question))](question)
        return self

    def save_questionnaire(self):
        """
        Function to save the questionnaire page

        return self
        """
        self.driver.find(SAVE_CHANGES_BTN).click()
        return self

    def create_default_question(self, question_data, question_link):
        """
        Function to define a default question on the questionnaire page

        Args:
        question_data is data to create a default entity question
        question_link is the locator for default question

        return self
        """
        self.driver.find(question_link).click()
        self.fill_question_and_code_tb(question_data)
        return self

    def fill_question_and_code_tb(self, question_data):
        """
        Function to fill the question and code text box on the questionnaire page

        Args:
        question_data is data to fill in the question and code text boxes

        return self
        """
        self.driver.find_text_box(QUESTION_TB).enter_text(fetch_(QUESTION, from_(question_data)))
        self.driver.find_text_box(CODE_TB).enter_text(fetch_(CODE, from_(question_data)))
        return self

    def configure_word_type_question(self, question_data):
        """
        Function to select word or phrase option and fill the details (min or max) on the questionnaire page

        Args:
        question_data is data to fill in the min and max fields

        return self
        """
        self.driver.find_radio_button(WORD_OR_PHRASE_RB).click()
        limit = fetch_(LIMIT, from_(question_data))
        if limit == LIMITED:
            self.driver.find_radio_button(CHARACTER_LIMIT_RB).click()
            self.driver.find_text_box(WORD_OR_PHRASE_MAX_LENGTH_TB).enter_text(fetch_(MAX, from_(question_data)))
        elif limit == NO_LIMIT:
            self.driver.find_radio_button(NO_CHARACTER_LIMIT_RB).click()
        return self

    def configure_number_type_question(self, question_data):
        """
        Function to select number option and fill the details (min or max) on the questionnaire page

        Args:
        question_data is data to fill in the min and max fields

        return self
        """
        self.driver.find_radio_button(NUMBER_RB).click()
        self.driver.find_text_box(NUMBER_MIN_LENGTH_TB).enter_text(fetch_(MIN, from_(question_data)))
        self.driver.find_text_box(NUMBER_MAX_LENGTH_TB).enter_text(fetch_(MAX, from_(question_data)))
        return self

    def configure_date_type_question(self, question_data):
        """
        Function to select date option and date format on the questionnaire page

        Args:
        question_data is data to select date type

        return self
        """
        self.driver.find_radio_button(DATE_RB).click()
        date_format = fetch_(DATE_FORMAT, from_(question_data))
        if (date_format == MM_YYYY):
            self.driver.find_radio_button(MONTH_YEAR_RB).click()
        elif (date_format == DD_MM_YYYY):
            self.driver.find_radio_button(DATE_MONTH_YEAR_RB).click()
        elif (date_format == MM_DD_YYYY):
            self.driver.find_radio_button(MONTH_DATE_YEAR_RB).click()
        return self

    def configure_list_of_choices_type_question(self, question_data):
        """
        Function to select list of choices option and add the choices on the questionnaire page

        Args:
        question_data is to add the choices on the page

        return self
        """
        self.driver.find_radio_button(LIST_OF_CHOICE_RB).click()
        index = 1
        for choice in fetch_(CHOICE, from_(question_data)):
            if index > 1:
                self.driver.find(ADD_CHOICE_LINK).click()
            self.driver.find_text_box(by_xpath(CHOICE_XPATH_LOCATOR + "[" + str(index) + "]" + CHOICE_TB_XPATH_LOCATOR)).enter_text(choice)
            index = index + 1
        choice_type = fetch_(ALLOWED_CHOICE, from_(question_data))
        if(ONLY_ONE_ANSWER == choice_type):
            self.driver.find_radio_button(ONLY_ONE_ANSWER_RB).click()
        elif(MULTIPLE_ANSWERS == choice_type):
            self.driver.find_radio_button(MULTIPLE_ANSWER_RB).click()
        return self

    def configure_geo_type_question(self, question_data):
        """
        Function to select geo option on the questionnaire page

        Args:
        question_data is data to select geo type

        return self
        """
        self.driver.find_radio_button(GEO_RB).click()
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

    def get_success_message(self):
        """
        Function to fetch the success message from label of the questionnaire page

        Return success message
        """
        comm_utils = CommonUtilities(self.driver)
        if comm_utils.wait_for_element(10, SUCCESS_MESSAGE_LABEL):
            return self.driver.find(SUCCESS_MESSAGE_LABEL).text
        else:
            return "Success message not appeared on the page."

    def get_remaining_character_count(self):
        """
        Function to fetch the remaining character count from label of the questionnaire page

        Return success message
        """
        return self.driver.find(CHARACTER_COUNT).text

    def get_question_link_text(self, question_number):
        """
        Function to get the text of the question link

        Args:
        question_number is index number of the question

        Return link text
        """
        question_locator = QUESTION_LINK_CSS_LOCATOR_PART1 + ":nth-child(" + str(question_number) + ")" + QUESTION_LINK_CSS_LOCATOR_PART2
        return self.driver.find(by_css(question_locator)).text
