# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from nose.plugins.attrib import attr
from nose.plugins.skip import SkipTest
from framework.base_test import BaseTest
from framework.utils.data_fetcher import fetch_, from_
from pages.loginpage.login_page import LoginPage
from testdata.test_data import DATA_WINNER_LOGIN_PAGE
from tests.logintests.login_data import VALID_CREDENTIALS
from tests.createquestionnairetests.create_questionnaire_data import *
from tests.createprojecttests.create_project_data import *
import time


class TestCreateQuestionnaire(BaseTest):

    def prerequisites_of_create_questionnaire(self):
        # doing successful login with valid credentials
        self.driver.go_to(DATA_WINNER_LOGIN_PAGE)
        login_page = LoginPage(self.driver)
        dashboard_page = login_page.do_successful_login_with(VALID_CREDENTIALS)
        # going on setup project page
        create_project_page = dashboard_page.navigate_to_create_project_page()
        #Navigating to Create Questionnaire Page by successfully creating a Project
        create_subject_questionnaire_page = create_project_page.successfully_create_project_with(VALID_DATA2)
        create_questionnaire_page = create_subject_questionnaire_page.successfully_create_subject_questionnaire_with(None)
        return create_questionnaire_page

    @attr('functional_test', 'smoke')
    def test_successful_questionnaire_creation(self):
        """
        Function to test the successful Creation of a Questionnaire with given details
        """
        create_questionnaire_page = self.prerequisites_of_create_questionnaire()
        create_questionnaire_page.create_questionnaire_with(QUESTIONNAIRE_DATA)
        index = 2
        for question in fetch_(QUESTIONS, from_(QUESTIONNAIRE_DATA)):
            question_link_text = fetch_(QUESTION, from_(question)) + " " + fetch_(CODE, from_(question))
            self.assertEquals(create_questionnaire_page.get_question_link_text(index), question_link_text)
            index = index + 1
        time.sleep(5)
        self.assertEquals(create_questionnaire_page.get_remaining_character_count(),
                          fetch_(CHARACTER_REMAINING, from_(QUESTIONNAIRE_DATA)))
        create_questionnaire_page.save_questionnaire()
        time.sleep(3)
        self.assertEqual(create_questionnaire_page.get_title(), "Data Senders")
