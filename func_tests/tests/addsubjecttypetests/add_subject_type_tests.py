# vim: ai ts=4 sts=4 et sw=4utf-8
from nose.plugins.attrib import attr
from framework.base_test import BaseTest
from framework.utils.data_fetcher import from_, fetch_
from pages.addsubjecttypepage.add_subject_type_page import AddSubjectTypePage
from pages.loginpage.login_page import LoginPage
from nose.plugins.skip import SkipTest
from testdata.test_data import DATA_WINNER_LOGIN_PAGE, DATA_WINNER_ADD_SUBJECT_TYPE
from tests.addsubjecttypetests.add_subject_type_data import *
from tests.logintests.login_data import VALID_CREDENTIALS


class TestAddSubjectType(BaseTest):

    def prerequisites_of_add_subject_type(self):
        # doing successful login with valid credentials
        self.driver.go_to(DATA_WINNER_LOGIN_PAGE)
        login_page = LoginPage(self.driver)
        login_page.do_successful_login_with(VALID_CREDENTIALS)
        self.driver.go_to(DATA_WINNER_ADD_SUBJECT_TYPE)
        return AddSubjectTypePage(self.driver)

    @attr('functional_test', 'smoke')
    def test_add_new_subject_type(self):
        add_subject_type_page = self.prerequisites_of_add_subject_type()
        add_subject_type_page.successfully_add_entity_type_with(VALID_ENTITY)
        self.assertEqual(add_subject_type_page.get_flash_message(), fetch_(SUCCESS_MESSAGE, from_(VALID_ENTITY)))

    @attr('functional_test')
    def test_add_existing_subject_type(self):
        add_subject_type_page = self.prerequisites_of_add_subject_type()
        add_subject_type_page.add_entity_type_with(ALREADY_EXIST_ENTITY)
        self.assertEqual(add_subject_type_page.get_flash_message(), fetch_(ERROR_MESSAGE, from_(ALREADY_EXIST_ENTITY)))

    @attr('functional_test')
    def test_add_blank_subject_type(self):
        add_subject_type_page = self.prerequisites_of_add_subject_type()
        add_subject_type_page.add_entity_type_with(BLANK)
        self.assertEqual(add_subject_type_page.get_error_message(), fetch_(ERROR_MESSAGE, from_(BLANK)))
