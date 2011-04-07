from framework.perspectives.Page import Page
from framework.utils.common_utils import CommonUtilities

__author__ = 'kumarr'

class HomePage(Page):

    def __init__(self, driver):
        Page.__init__(self, driver)

    def goToHomePage(self):
        self.driver.get("https://www.bcgperspectives.com/")

    def clickOnRegistrationLinkAndNavigateToRegistrationOverlay(self):
        CommonUtilities(self.driver).findElementAndClick('register')
        CommonUtilities(self.driver).waitForElement(5, 'overlay_form')

    def clickOnLoginLinkAndNavigateToLoginOverlay(self):
        CommonUtilities(self.driver).findElementAndClick("login")
        CommonUtilities(self.driver).waitForElement(5, 'login_overlay_form')
  