# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from nose.plugins.attrib import attr
from nose.plugins.skip import SkipTest
from framework.base_test import BaseTest
from framework.utils.data_fetcher import fetch_, from_
from pages.createprojectpage.create_project_page import CreateProjectPage
from pages.loginpage.login_page import LoginPage
from pages.createquestionnairepage.create_questionnaire_page import CreateQuestionnairePage
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
        CreateProjectPage = dashboard_page.navigate_to_create_project_page()
        #Navigating to Create Questionnaire Page by successfully creating a Project
        CreateQuestionnairePage = CreateProjectPage.successfully_create_project_with(VALID_DATA)
        return CreateQuestionnairePage

    @attr('functional_test')
    def test_successful_questionnaire_creation(self):
        """
        Function to test the successful Creation of a Questionnaire with given
        details
        """
        create_questionnaire_page = self.prerequisites_of_create_questionnaire()
        create_questionnaire_page.create_questionnaire_with(QUESTIONNAIRE_DATA)
        time.sleep(2)
        self.assertEqual(create_questionnaire_page.get_success_message(),
                                 fetch_(SUCCESS_MSG, from_(QUESTIONNAIRE_DATA)))
