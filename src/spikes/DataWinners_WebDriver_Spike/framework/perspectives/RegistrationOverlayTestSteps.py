__author__ = 'ravi'

from framework.perspectives.Page import Page
from framework.utils.commonUtils import CommonUtilities

class RegistrationOverlay(Page):

    def __init__(self, driver):
        Page.__init__(self, driver)

    def verifyEmailValidationErrorMessageIfEmailAddressNotEntered(self):
        

        CommonUtilities(self.driver).findTextBoxAndEnterText('Password',"!4321abcd")
        CommonUtilities(self.driver).findTextBoxAndEnterText("ConfirmPassword", "!4321abcd")
        CommonUtilities(self.driver).findTextBoxAndEnterText("FirstName", "Gim")
        CommonUtilities(self.driver).findTextBoxAndEnterText("LastName", "Green")
        CommonUtilities(self.driver).findDropDownAndSelectOption("Country", "Albania")
        #CommonUtilities(self.driver).findTextBoxAndEnterText("ScreenName", "GimGreen")
        CommonUtilities(self.driver).findElementAndClick("registersubmit")
        CommonUtilities(self.driver).waitForElement(5, 'emailError')
        CommonUtilities(self.driver).validateErrorMessage('emailError','Please enter a valid e-mail address.')
        print "Email error message is present"
        return self

    def verifyUserSeesInterestAndAlertsScreen(self):
        CommonUtilities(self.driver).waitForElement(5, 'overlay_form')
        self.driver.find_element_by_id('Email').send_keys("ravi3010@gmail.com")
        self.driver.find_element_by_id('Password').send_keys("abcde")
        self.driver.find_element_by_id('ConfirmPassword').send_keys("abcde")
        self.driver.find_element_by_id('FirstName').send_keys("Gim")
        self.driver.find_element_by_id('LastName').send_keys("Green")
        self.driver.find_drop_down("Country").set_selected("Albania")
        self.driver.find_element_by_id('ScreenName').send_keys("Green")
        self.driver.find_element_by_id('registersubmit').click()
        CommonUtilities(self.driver).waitForElement(5, 'registercomplete')
        
        return self
#
