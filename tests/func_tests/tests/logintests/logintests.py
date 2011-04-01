from framework.baseTest import BaseTest
from framework.mangrovetests.logintests import LoginPage


__author__ = 'kumarr'


class LoginPageTests(BaseTest) :

    def test_LoginWithValidCredentials(self):

        self.driver.get("http://localhost:8000/login")
        loginPage = LoginPage(self.driver)
        dashboardPage= loginPage.SuccessfulLogin("nogo@mail.com", "nogo123")
        self.assertEqual(dashboardPage.WelcomeMessage(), "Welcome No Go", "Login Un-successful or UserName is not Present")


    def test_LoginWithInvalidEmailAddressCredential(self):

        self.driver.get("http://localhost:8000/login")
        loginPage = LoginPage(self.driver)
        loginPage.EnterCredentialsAndSubmit("invalid@mail", "nogo123")
        self.assertEqual(loginPage.GetErrorMessage(), "Enter a valid e-mail address.")

    def test_LoginWithInvalidPasswordCredential(self):

        self.driver.get("http://localhost:8000/login")
        loginPage = LoginPage(self.driver)
        loginPage.EnterCredentialsAndSubmit("invalid@mail.com", "nogo123")
        self.assertEqual(loginPage.GetErrorMessage(), "Email and password do not match!!!")


    def test_LoginWithoutEnteringEmailAddress(self):

        self.driver.get("http://localhost:8000/login")
        loginPage = LoginPage(self.driver)
        loginPage.EnterCredentialsAndSubmit("", "nogo123")
        self.assertEqual(loginPage.GetErrorMessage(), "email This field is required.")


    def test_LoginWithoutEnteringPassword(self):

        self.driver.get("http://localhost:8000/login")
        loginPage = LoginPage(self.driver)
        loginPage.EnterCredentialsAndSubmit("nogo@mail.com", "")
        self.assertEqual(loginPage.GetErrorMessage(), "password This field is required.")

    def test_LoginWithoutEnteringEmailAndPassword(self):

        self.driver.get("http://localhost:8000/login")
        loginPage = LoginPage(self.driver)
        loginPage.EnterCredentialsAndSubmit("","")
        self.assertEqual(loginPage.GetErrorMessage(), "This field is required. This field is required.")

    def test_RegisterLinkFunctionality(self):

        self.driver.get("http://localhost:8000/login")
        loginPage = LoginPage(self.driver)
        registerPage=loginPage.NavigateToRegistrationPage()
        self.assertEqual(registerPage.GetTitle(), "Register", "Registration Page Title is incorrect or Register Link is Not Working")


