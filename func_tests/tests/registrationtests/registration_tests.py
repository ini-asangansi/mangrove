from framework.base_test import BaseTest
from framework.mangrovetests.registration_page import RegistrationPage
from nose.tools import *




__author__ = 'kumarr'


class TestRegistrationPage(BaseTest) :

    def test_register_ngo_with_valid_data(self):

        self.driver.get("http://localhost:8000/register")
        registration_page = RegistrationPage(self.driver)
        registration_confirmation_page = registration_page.enter_data_in_all_fields_and_click_register( "NGO 001", "PublicHealth", "Address Line One", "Address Line Two", "Pune", "Maharashtra", "India", "411028", "0123456789", "http://ngo001.com", "Mr", "No", "Go", "ngo001@ngo.com", "ngo001", "ngo001")
        eq_(registration_confirmation_page.registration_success_message(), "You have successfully registered organization with id : 1234.", "Organization Name is incorrect or not displayed on Registration Confirmation Page")

