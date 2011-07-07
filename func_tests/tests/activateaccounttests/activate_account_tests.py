# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from nose.plugins.attrib import attr
from nose.plugins.skip import SkipTest
from framework.base_test import BaseTest
from framework.utils.couch_http_wrapper import CouchHttpWrapper
from framework.utils.data_fetcher import fetch_, from_
from pages.registrationpage.registration_page import RegistrationPage
from testdata.test_data import DATA_WINNER_REGISTER_PAGE
from tests.registrationtests.registration_data import REGISTRATION_DATA_FOR_SUCCESSFUL_REGISTRATION
from tests.activateaccounttests.activate_account_data import *
from pages.activateaccountpage.activate_account_page import ActivateAccountPage
from framework.utils.database_manager_postgres import DatabaseManager


class TestActivateAccount(BaseTest):

    def prerequisites_of_activate_account(self):
        self.driver.go_to(DATA_WINNER_REGISTER_PAGE)
        registration_page = RegistrationPage(self.driver)
        registration_confirmation_page, self.email = registration_page.successful_registration_with(REGISTRATION_DATA_FOR_SUCCESSFUL_REGISTRATION)
        self.assertEquals(registration_confirmation_page.registration_success_message(),
            fetch_(SUCCESS_MESSAGE, from_(REGISTRATION_DATA_FOR_SUCCESSFUL_REGISTRATION)))
        return self.email

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

    @attr('functional_test', 'smoke')
    def test_successful_activation_of_account(self):
        """
        Function to test the successful activation of account with given details
        """
        email = self.prerequisites_of_activate_account()
        account_activate_page = ActivateAccountPage(self.driver)
        dbmanager = DatabaseManager()
        activation_code = dbmanager.get_activation_code(email)
        account_activate_page.activate_account(activation_code)
        self.assertRegexpMatches(account_activate_page.get_message(), fetch_(SUCCESS_MESSAGE, from_(VALID_ACTIVATION_DETAILS)))
