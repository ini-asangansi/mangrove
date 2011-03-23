from framework.openMangrove.Page import Page

__author__ = 'kumarr'


class LoginPage(Page):

    def __init__(self, driver):
        Page.__init__(self, driver)

    def enterCredentialsAndSubmit(self, emailId, password):
        self.driver.find_text_box("email").enter_text(emailId)
        self.driver.find_text_box("password").enter_text(password)
        self.driver.find_element_by_name("submit").click()
        return self

        