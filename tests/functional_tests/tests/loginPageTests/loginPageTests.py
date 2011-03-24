from framework.baseTest import BaseTest
from framework.openMangrove.LoginPage import LoginPage
from framework.openMangrove.DashboardPage import DashboardPage
from framework.openMangrove.RegistrationPage import RegistrationPage

__author__ = 'kumarr'


class LoginPageTests(BaseTest) :

    def test_LoginWithValidCredentials(self):

        self.driver.get("http://localhost:8000/login")
        loginPage = LoginPage(self.driver)
        loginPage.EnterCredentialsAndSubmit("nogo@mail.com", "nogo123")
        self.assertEqual(DashboardPage(self.driver).WelcomeMessage(), "Welcome No Go", "Login Un-successful or UserName is not Present")


    def test_LoginWithInvalidEmailAddressCredential(self):

        self.driver.get("http://localhost:8000/login")
        loginPage = LoginPage(self.driver)
        loginPage.EnterCredentialsAndSubmit("invalid@mail.com", "nogo123")
        self.assertEqual(LoginPage(self.driver).GetErrorMessage(), "Email and password do not match!!!", "Error Message Not Present/Incorrect")

    def test_LoginWithInvalidPasswordCredential(self):

        self.driver.get("http://localhost:8000/login")
        loginPage = LoginPage(self.driver)
        loginPage.EnterCredentialsAndSubmit("invalid@mail.com", "nogo123")
        self.assertEqual(LoginPage(self.driver).GetErrorMessage(), "Email and password do not match!!!", "Error Message Not Present/Incorrect")


    def test_LoginWithoutEnteringEmailAddress(self):

        self.driver.get("http://localhost:8000/login")
        loginPage = LoginPage(self.driver)
        loginPage.EnterCredentialsAndSubmit("", "nogo123")
        self.assertEqual(LoginPage(self.driver).GetErrorMessage(), "email This field is required.", "Error Message Not Present")


    def test_LoginWithoutEnteringPassword(self):

        self.driver.get("http://localhost:8000/login")
        loginPage = LoginPage(self.driver)
        loginPage.EnterCredentialsAndSubmit("nogo@mail.com", "")
        self.assertEqual(LoginPage(self.driver).GetErrorMessage(), "password This field is required.", "Error Message Not Present")

    def test_loginWithoutEnteringEmailAndPassword(self):

        self.driver.get("http://localhost:8000/login")
        loginPage = LoginPage(self.driver)
        loginPage.EnterCredentialsAndSubmit("","")
        self.assertEqual(LoginPage(self.driver).GetErrorMessage(), "password This field is required. email This field is required.", "Error Message Not Present")

    def test_RegisterLinkFunctionality(self):

        self.driver.get("http://localhost:8000/login")
        loginPage = LoginPage(self.driver)
        loginPage.NavigateToRegistrationPage()
        self.assertEqual(RegistrationPage(self.driver).GetTitle(), "Register", "Registration Page Title is incorrect or Register LinkLink is Not Working")


