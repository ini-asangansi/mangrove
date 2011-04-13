# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from framework.base_test import BaseTest
from framework.pages.registrationpage.registration_page import RegistrationPage
from nose.tools import *
from registration_data import *
from nose.plugins.skip import SkipTest


__author__ = 'kumarr'

#@SkipTest
class TestRegistrationPage(BaseTest) :

    def test_successful_registration(self):

        self.driver.get("http://localhost:8000/register")
        registration_page = RegistrationPage(self.driver)
        registration_confirmation_page = registration_page.do_successful_registration(REGISTRATION_DATA_FOR_SUCCESSFUL_REGISTRATION)
        eq_(registration_confirmation_page.registration_success_message(), "You have successfully registered!!", "Organization Name is incorrect or not displayed on Registration Confirmation Page")


    def test_register_ngo_with_existing_email_address(self):
        self.driver.get("http://localhost:8000/register")
        registration_page = RegistrationPage(self.driver)
        registration_page = registration_page.enter_existing_email_id_and_click_register(REGISTRATION_DATA_FOR_EXISTING_EMAIL_ERROR)
        eq_(registration_page.existing_email_error_message(), "This email address is already in use. Please supply a different email address.", "Error Message for existing email id is not present or incorrect")



#    def test_register_ngo_with_