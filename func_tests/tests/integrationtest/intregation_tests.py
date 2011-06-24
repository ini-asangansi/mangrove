# vim: ai ts=4 sts=4 et sw=4utf-8
import time
from nose.plugins.attrib import attr
from framework.base_test import BaseTest
from framework.utils.common_utils import get_epoch_last_ten_digit
from framework.utils.couch_http_wrapper import CouchHttpWrapper
from framework.utils.data_fetcher import from_, fetch_
from framework.utils.database_manager import DatabaseManager
from pages.activateaccountpage.activate_account_page import ActivateAccountPage
from pages.addsubjecttypepage.add_subject_type_page import AddSubjectTypePage
from pages.loginpage.login_page import LoginPage
from nose.plugins.skip import SkipTest
from pages.smstesterpage.sms_tester_page import SMSTesterPage
from testdata.test_data import DATA_WINNER_LOGIN_PAGE, DATA_WINNER_ADD_SUBJECT_TYPE, DATA_WINNER_HOME_PAGE, DATA_WINNER_SMS_TESTER_PAGE
from tests.integrationtest.intregation_data import *


class TestIntregationOfApplication(BaseTest):

    def tearDown(self):
        try:
            self.driver.quit()
            email = self.email
            dbmanager = DatabaseManager()
            dbname = dbmanager.delete_organization_all_details(email)
            couchwrapper = CouchHttpWrapper("localhost")
            couchwrapper.deleteDb(dbname)
        except TypeError as e:
            pass

    @attr('functional_test', 'smoke', "intregation")
    def test_intregation_of_application(self):

        self.driver.go_to(DATA_WINNER_LOGIN_PAGE)
        login_page = LoginPage(self.driver)
        registration_page = login_page.navigate_to_registration_page()
        self.assertEqual(registration_page.get_title(), "Register")

        registration_confirmation_page, self.email = registration_page.successful_registration_with(REGISTRATION_DATA_FOR_SUCCESSFUL_REGISTRATION)
        self.assertEquals(registration_confirmation_page.registration_success_message(),
            fetch_(SUCCESS_MESSAGE, from_(REGISTRATION_DATA_FOR_SUCCESSFUL_REGISTRATION)))

        dbmanager = DatabaseManager()
        organization_sms_tel_number = get_epoch_last_ten_digit()
        dbmanager.set_sms_telephone_number(organization_sms_tel_number, self.email)

        account_activate_page = ActivateAccountPage(self.driver)
        dbmanager = DatabaseManager()
        activation_code = dbmanager.get_activation_code(self.email)
        account_activate_page.activate_account(activation_code)
        self.assertRegexpMatches(account_activate_page.get_message(), fetch_(SUCCESS_MESSAGE, from_(VALID_ACTIVATION_DETAILS)))

        self.driver.go_to(DATA_WINNER_LOGIN_PAGE)
        VALID_LOGIN_CREDENTIALS = VALID_CREDENTIALS
        VALID_LOGIN_CREDENTIALS[USERNAME] = self.email
        dashboard_page = login_page.do_successful_login_with(VALID_LOGIN_CREDENTIALS)
        self.assertEqual(dashboard_page.welcome_message(), fetch_(WELCOME_MESSAGE, from_(VALID_LOGIN_CREDENTIALS)))

        register_reporter_page = dashboard_page.navigate_to_register_reporter_page()
        register_reporter_page.register_with(VALID_DATA_FOR_REPORTER)
        self.assertRegexpMatches(register_reporter_page.get_success_message(), fetch_(SUCCESS_MESSAGE, from_(VALID_DATA_FOR_REPORTER)))

        self.driver.go_to(DATA_WINNER_ADD_SUBJECT_TYPE)
        add_subject_type_page = AddSubjectTypePage(self.driver)
        add_subject_type_page.add_entity_type_with(VALID_SUBJECT_TYPE1)
        self.assertEqual(add_subject_type_page.get_flash_message(), fetch_(SUCCESS_MESSAGE, from_(VALID_SUBJECT_TYPE1)))
        add_subject_type_page.add_entity_type_with(VALID_SUBJECT_TYPE2)
        self.assertEqual(add_subject_type_page.get_flash_message(), fetch_(SUCCESS_MESSAGE, from_(VALID_SUBJECT_TYPE2)))

        self.driver.go_to(DATA_WINNER_HOME_PAGE)
        register_subject_page = dashboard_page.navigate_to_register_subject_page()
        message = register_subject_page.successfully_register_subject_with(VALID_DATA_FOR_SUBJECT)
        self.assertRegexpMatches(register_subject_page.get_flash_message(), message)

        self.driver.go_to(DATA_WINNER_HOME_PAGE)
        create_project_page = dashboard_page.navigate_to_create_project_page()
        create_subject_questionnaire_page = create_project_page.successfully_create_project_with(VALID_DATA_FOR_PROJECT)
        self.assertRegexpMatches(create_subject_questionnaire_page.get_title(),
                                 fetch_(PAGE_TITLE, from_(VALID_DATA_FOR_PROJECT)))

        create_questionnaire_page = create_subject_questionnaire_page.successfully_create_subject_questionnaire_with(None)
        self.assertRegexpMatches(create_questionnaire_page.get_title(),
                                 fetch_(PAGE_TITLE, from_(VALID_DATA_FOR_SUBJECT_QUESTIONNAIRE)))

        create_questionnaire_page.create_questionnaire_with(QUESTIONNAIRE_DATA)
        self.assertEqual(create_questionnaire_page.get_success_message(),
                                 fetch_(SUCCESS_MESSAGE, from_(QUESTIONNAIRE_DATA)))
        index = 2
        for question in fetch_(QUESTIONS, from_(QUESTIONNAIRE_DATA)):
            question_link_text = fetch_(QUESTION, from_(question)) + " " + fetch_(CODE, from_(question))
            self.assertEquals(create_questionnaire_page.get_question_link_text(index), question_link_text)
            index = index + 1
        time.sleep(5)
        self.assertEquals(create_questionnaire_page.get_remaining_character_count(),
                          fetch_(CHARACTER_REMAINING, from_(QUESTIONNAIRE_DATA)))

        self.driver.go_to(DATA_WINNER_SMS_TESTER_PAGE)
        sms_tester_page = SMSTesterPage(self.driver)
        sms_tester_data = VALID_DATA_FOR_SMS
        sms_tester_data[RECEIVER] = organization_sms_tel_number
        sms_tester_page.send_sms_with(sms_tester_data)
        self.assertEqual(sms_tester_page.get_response_message(), fetch_(SUCCESS_MESSAGE, from_(sms_tester_data)))

        self.driver.go_to(DATA_WINNER_HOME_PAGE)
        view_all_project_page = dashboard_page.navigate_to_view_all_project_page()
        time.sleep(3)
        project_overview_project = view_all_project_page.navigate_to_project_page(fetch_(PROJECT_NAME, VALID_DATA_FOR_PROJECT))
        submission_log_page = project_overview_project.navigate_to_submission_log_page()
        self.assertRegexpMatches(submission_log_page.get_title(), "Activity Log")
        time.sleep(3)
        self.assertRegexpMatches(submission_log_page.get_submission_message(SMS_DATA_LOG), fetch_(SMS_SUBMISSION, from_(SMS_DATA_LOG)))

        self.driver.go_to(DATA_WINNER_SMS_TESTER_PAGE)
        sms_tester_data = VALID_DATA_FOR_SMS
        sms_tester_data[RECEIVER] = organization_sms_tel_number
        sms_tester_page.send_sms_with(sms_tester_data)
        self.assertEqual(sms_tester_page.get_response_message(), fetch_(SUCCESS_MESSAGE, from_(sms_tester_data)))
