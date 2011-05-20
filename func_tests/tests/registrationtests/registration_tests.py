# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from nose.plugins.attrib import attr

from framework.base_test import BaseTest
from framework.utils.data_fetcher import fetch_, from_
from pages.registrationpage.registration_page import RegistrationPage
from registration_data import *
from testdata.test_data import DATA_WINNER_REGISTER_PAGE


class TestRegistrationPage(BaseTest):

    @attr('functional_test', 'smoke')
    def test_successful_registration(self):

        self.driver.go_to(DATA_WINNER_REGISTER_PAGE)
        registration_page = RegistrationPage(self.driver)
        registration_confirmation_page = registration_page.successful_registration_with(REGISTRATION_DATA_FOR_SUCCESSFUL_REGISTRATION)
        self.assertEquals(registration_confirmation_page.registration_success_message(),
            fetch_(SUCCESS_MESSAGE,
                   from_(REGISTRATION_DATA_FOR_SUCCESSFUL_REGISTRATION)))

    @attr('functional_test')
    def test_register_ngo_with_existing_email_address(self):
        self.driver.go_to(DATA_WINNER_REGISTER_PAGE)
        registration_page = RegistrationPage(self.driver)
        registration_page.register_with(EXISTING_EMAIL_ADDRESS)
        self.assertEquals(registration_page.get_error_message(), fetch_(ERROR_MESSAGE,
                   from_(EXISTING_EMAIL_ADDRESS)))

    @attr('functional_test')
    def test_register_ngo_with_invalid_email_address(self):
        self.driver.go_to(DATA_WINNER_REGISTER_PAGE)
        registration_page = RegistrationPage(self.driver)
        registration_page.register_with(INVALID_EMAIL_FORMAT)
        self.assertEquals(registration_page.get_error_message(),
                          fetch_(ERROR_MESSAGE, from_(INVALID_EMAIL_FORMAT)))

    @attr('functional_test')
    def test_register_ngo_with_unmatched_passwords(self):
        self.driver.go_to(DATA_WINNER_REGISTER_PAGE)
        registration_page = RegistrationPage(self.driver)
        registration_page.register_with(UNMATCHED_PASSWORD)
        self.assertEquals(registration_page.get_error_message(),
                          fetch_(ERROR_MESSAGE, from_(UNMATCHED_PASSWORD)))

    @attr('functional_test')
    def test_register_ngo_without_entering_data(self):
        self.driver.go_to(DATA_WINNER_REGISTER_PAGE)
        registration_page = RegistrationPage(self.driver)
        registration_page.register_with(WITHOUT_ENTERING_REQUIRED_FIELDS)
        self.assertEquals(registration_page.get_error_message(),
                          fetch_(ERROR_MESSAGE, from_(WITHOUT_ENTERING_REQUIRED_FIELDS)))

    @attr('functional_test')
    def test_register_ngo_with_invalid_web_url(self):
        self.driver.go_to(DATA_WINNER_REGISTER_PAGE)
        registration_page = RegistrationPage(self.driver)
        registration_page.register_with(INVALID_WEBSITE_URL)
        self.assertEquals(registration_page.get_error_message(),
                          fetch_(ERROR_MESSAGE, from_(INVALID_WEBSITE_URL)))
