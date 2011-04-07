from framework.baseTest import BaseTest
from framework.mangrovetests.dashboard_tests import DashboardPage
from framework.mangrovetests.login_page import LoginPage

__author__ = 'kumarr'


class LoginPageTests(BaseTest) :

    def test_RegisterNGOWithValidData(self):

        self.driver.get("http://localhost:8000/login")
        loginPage = LoginPage(self.driver)

        loginPage.EnterCredentialsAndSubmit("nogo@mail.com", "nogo123")
        self.assertEqual(DashboardPage(self.driver).WelcomeMessage(), "No Go!", "Login Un-successful or UserName is not Present")