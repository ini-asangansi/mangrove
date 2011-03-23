from framework.baseTest import BaseTest
from framework.openMangrove.LoginPage import LoginPage
from framework.openMangrove.DashboardPage import DashboardPage

__author__ = 'kumarr'


class LoginPageTests(BaseTest) :

    def test_LoginFunctionality(self):

        self.driver.get("http://localhost:8000/login")
        loginPage = LoginPage(self.driver)
        loginPage.enterCredentialsAndSubmit("nogo@mail.com", "nogo123")
        self.assertEqual(DashboardPage(self.driver).LoginSuccessfulMessage(), "Password accepted!", "Login successful message is not present or incorrect")
