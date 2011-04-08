from framework.base_test import BaseTest
from nose.tools import *
from framework.mangrovetests.registration_page import RegistrationPage



__author__ = 'kumarr'


class LoginPageTests(BaseTest) :

    def test_register_ngo_with_valid_data(self):

        register_page = self.driver.get("http://localhost:8000/register")

        registration_conformation_page = RegistrationPage(self.driver).enter_data_in_all_fields_and_click_register( "NGO 001",
                                                                                                                    "PublicHealth",
                                                                                                                    "Address Line One",
                                                                                                                    "Address Line Two",
                                                                                                                    "Pune",
                                                                                                                    "Maharashtra",
                                                                                                                    "India",
                                                                                                                    "411028",
                                                                                                                    "0123456789",
                                                                                                                    "http://ngo001.com",
                                                                                                                    "Mr",
                                                                                                                    "No",
                                                                                                                    "Go",
                                                                                                                    "ngo001@ngo.com",
                                                                                                                    "ngo001",
                                                                                                                    "ngo001")
        eq_(registration_conformation_page.organization_name(), "No Go 2", "Organization Name is incorrect or not displayed on Registration Confirmation Page")

