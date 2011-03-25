from framework.baseTest import BaseTest
from framework.shoppersStop.RegistrationPage import RegistrationPage

__author__ = 'anandb'

class RegistrationTest(BaseTest):

    def test_RegisterButtonFunctionality(self):
        self.driver.get("https://www.shoppersstop.com/accountRegister.jsp.vr")
        self.assertTrue(RegistrationPage(self.driver).findRadioButtonAndValidateStatus('gender_male', True))

    def test_ValidateErrorMessageIfPasswordIsNotProvided(self):
        self.driver.get("https://www.shoppersstop.com/accountRegister.jsp.vr")
        self.assertTrue(RegistrationPage(self.driver).NoPasswordEnteredAndRegister().validateErrorMessagesContains("Please enter a valid password."))
        self.assertTrue(RegistrationPage(self.driver).validateErrorMessagesContains("Please enter a valid password."))

    def test_ValidateErrorMessageIfEmailIsNotProvided(self):
        self.driver.get("https://www.shoppersstop.com/accountRegister.jsp.vr")
        self.assertTrue(RegistrationPage(self.driver).NoEmailEnteredAndRegister().validateErrorMessage("Please enter a email address"))



