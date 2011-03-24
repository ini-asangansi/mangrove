from framework.baseTest import BaseTest

__author__ = 'kumarr'


class LoginPageTests(BaseTest) :

    def test_RegisterAnNGOWithValidData(self):

        self.driver.get("http://localhost:8000/login")
        loginPage = LoginPage(self.driver)

        loginPage.EnterCredentialsAndSubmit("nogo@mail.com", "nogo123")
        self.assertEqual(DashboardPage(self.driver).WelcomeMessage(), "No Go!", "Login Un-successful or UserName is not Present")