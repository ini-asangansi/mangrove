
from framework.baseTest import BaseTest
from framework.mangrovetests.login_page import LoginPage
from nose.tools import *

__author__ = 'kumarr'


class TestLoginPage(BaseTest):

    def test_login_with_valid_credentials(self):

        self.driver.get("http://localhost:8000/login")
        loginPage = LoginPage(self.driver)
        dashboardPage= loginPage.successful_login("nogo@mail.com", "nogo123")
        eq_(dashboardPage.welcome_message(), "Welcome Mr. No Go",
          "Login Un-successful or UserName is not Present")


    def test_login_with_invalid_email_address(self):

        self.driver.get("http://localhost:8000/login")
        loginPage = LoginPage(self.driver)
        loginPage.enter_credentials_and_submit("invalid@mail", "nogo123")
        self.assertEqual(loginPage.get_error_message(),
                         "Enter a valid e-mail address.")

    def test_login_with_invalid_password_credential(self):

        self.driver.get("http://localhost:8000/login")
        loginPage = LoginPage(self.driver)
        loginPage.enter_credentials_and_submit("invalid@mail.com", "nogo123")
        self.assertEqual(loginPage.get_error_message(),
                         "Email and password do not match!!!")


    def test_login_without_entering_email_address(self):

        self.driver.get("http://localhost:8000/login")
        loginPage = LoginPage(self.driver)
        loginPage.EnterCredentialsAndSubmit("", "nogo123")
        self.assertEqual(loginPage.GetErrorMessage(), "email This field is required.")


    def test_login_without_entering_password(self):

        self.driver.get("http://localhost:8000/login")
        loginPage = LoginPage(self.driver)
        loginPage.EnterCredentialsAndSubmit("nogo@mail.com", "")
        self.assertEqual(loginPage.GetErrorMessage(), "password This field is required.")

    def test_login_without_entering_email_and_password(self):

        self.driver.get("http://localhost:8000/login")
        loginPage = LoginPage(self.driver)
        loginPage.EnterCredentialsAndSubmit("","")
        self.assertEqual(loginPage.GetErrorMessage(), "This field is required. This field is required.")

    def test_register_link_functionality(self):

        self.driver.get("http://localhost:8000/login")
        loginPage = LoginPage(self.driver)
        registerPage=loginPage.NavigateToRegistrationPage()
        self.assertEqual(registerPage.GetTitle(), "Register", "Registration Page Title is incorrect or Register Link is Not Working")


