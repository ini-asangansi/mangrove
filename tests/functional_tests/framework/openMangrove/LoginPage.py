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

    def SubmitWithoutEnteringEmailAndPassword(self):
        self.driver.find_element_by_css_selector("input[value='Login']").click()
        return self

    def InvalidCredentialErrorMessage(self):
        invalidEmailErrorMessage = self.driver.find_element_by_class_name("error span-12 push-6 message-box").text
        return invalidEmailErrorMessage

    def EmailAddressNotPresentErrorMessage(self):
        emailAddressNotPresentErrorMessage = self.driver.find_element_by_css_selector(".errorlist li").text
        emailAddressNotPresentErrorMessage = emailAddressNotPresentErrorMessage.replace("\n", "")
        return emailAddressNotPresentErrorMessage

    def PasswordNotPresentErrorMessage(self):
        passwordNotPresentErrorMessage = self.driver.find_element_by_css_selector(".errorlist li").text
        passwordNotPresentErrorMessage = passwordNotPresentErrorMessage.replace("\n", "")
        return passwordNotPresentErrorMessage

    def EmailAndPasswordNotPresentErrorMessage(self):
        emailAndPasswordNotPresentErrorMessage = self.driver.find_element_by_xpath("//div[@class='error span-12 push-6 message-box']").text
        emailAndPasswordNotPresentErrorMessage = emailAndPasswordNotPresentErrorMessage.replace("\n", "")
        return emailAndPasswordNotPresentErrorMessage

