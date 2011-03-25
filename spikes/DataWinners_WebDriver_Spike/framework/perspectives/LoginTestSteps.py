


from framework.perspectives.Page import Page
from framework.utils.commonUtils import CommonUtilities


__author__ = 'kumarr'

class LoginOverlay(Page):

    def __init__(self, driver):
        Page.__init__(self, driver)

    def verifyValidationErrorMessageIfEmailAddressAndPasswordBothNotEntered(self):
        CommonUtilities(self.driver).findElementAndClick('login_button')
        CommonUtilities(self.driver).validateErrorMessage("errorcontainer", "Please enter both your e-mail and password.")

        return self