from framework.openMangrove.Page import Page
import time


__author__ = 'kumarr'


class LoginPage(Page):

    def __init__(self, driver):
        Page.__init__(self, driver)

    def EnterCredentialsAndSubmit(self, emailId, password):
        self.driver.find_text_box("email").enter_text(emailId)
        self.driver.find_text_box("password").enter_text(password)
        self.driver.find_element_by_css_selector("input[value='Login']").click()
        return self

    def GetErrorMessage(self):
        errorMessage = self.driver.find_element_by_css_selector("div[class*=error]").text
        errorMessage = errorMessage.replace("\n", " ")
        return errorMessage

    def NavigateToRegistrationPage(self):
        self.driver.find_element_by_css_selector("a[href='/register']").click()
        return self





