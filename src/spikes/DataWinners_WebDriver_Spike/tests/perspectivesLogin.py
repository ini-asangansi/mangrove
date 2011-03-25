from framework.baseTest import BaseTest
from framework.perspectives.HomePageTestSteps import HomePage
from framework.perspectives.LoginTestSteps import LoginOverlay

__author__ = 'kumarr'

class perspectivesLoginTests(BaseTest):

    def test_LoginWithInvalidPasswordAndVerifyErrorMessage(self):
        HomePage(self.driver).goToHomePage() #On Home Page
        HomePage(self.driver).clickOnLoginLinkAndNavigateToLoginOverlay() #Click on Login Link to Navigate to Login Overlay
        LoginOverlay(self.driver).verifyValidationErrorMessageIfEmailAddressAndPasswordBothNotEntered() #Hit Enter without providing Email and Password and Verify Error Message.