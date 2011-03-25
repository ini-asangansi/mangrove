from framework.baseTest import BaseTest
from framework.perspectives.HomePageTestSteps import HomePage
from framework.perspectives.RegistrationOverlayTestSteps import RegistrationOverlay

__author__ = 'Kumarr'

class perspectivesRegistrationTest(BaseTest):

    def test_EmailErrorMessageOnRegistrationOverlay(self): #This test verifies that On Registration Overlay, App throws Error Message if User doesn't provide Email Address and clicks on "Next" Button
        HomePage(self.driver).goToHomePage() #On Home Page
        HomePage(self.driver).clickOnRegistrationLinkAndNavigateToRegistrationOverlay() #Navigate To Registration OverLay
        RegistrationOverlay(self.driver).verifyEmailValidationErrorMessageIfEmailAddressNotEntered() # Enter Other Mandatory Fields and Validate Error Message

    def test_NavigatingToInterestAndAlertsScreenOfRegistrationOverlay(self):#This test verifies that User is taken to the Second screen on Registration Overlay if User fills/selects All Mandatory Fields.
        HomePage.goToHomePage() #On Home Page
        HomePage(self.driver).clickOnRegistrationLinkAndNavigateToRegistrationOverlay() #Navigate To Registration OverLay
        RegistrationOverlay(self.driver).verifyUserSeesInterestAndAlertsScreen() # Enter Other Mandatory Fields and Verify that User is on Interest And Alerts Screen of Registration Overlay
