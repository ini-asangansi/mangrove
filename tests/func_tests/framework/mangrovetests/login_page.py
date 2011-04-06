from framework.mangrovetests.page import Page
from framework.mangrovetests.dashboard_tests import DashboardPage
from framework.mangrovetests.registrationpage import  RegistrationPage
from framework.utils.commonUtils import CommonUtilities
from selenium.webdriver.common.by import By

__author__ = 'kumarr'


class LoginPage(Page):

    def __init__(self, driver):
        Page.__init__(self, driver)

    def SuccessfulLogin(self, emailId, password):
        self.driver.find_text_box("email").enter_text(emailId)
        self.driver.find_text_box("password").enter_text(password)
        self.driver.find_element_by_css_selector("input[value='Login']").click()
        return DashboardPage(self.driver)

    def EnterCredentialsAndSubmit(self, emailId, password):
        self.driver.find_text_box("email").enter_text(emailId)
        self.driver.find_text_box("password").enter_text(password)
        self.driver.find_element_by_css_selector("input[value='Login']").click()
        return self

    def GetErrorMessage(self):
        errorMessage1 = None
        errorMessage2 = None
        errorMessage = ""
        locator1 = CommonUtilities(self.driver).isElementPresent("div[class*='error']>input#id_email+ul>li",By.CSS_SELECTOR)
        if locator1:
            errorMessage1 = locator1.text

        locator2 = CommonUtilities(self.driver).isElementPresent("div[class*='error']>input#id_password+ul>li",By.CSS_SELECTOR)
        if locator2:
            errorMessage2 = locator2.text

        if errorMessage1:
            errorMessage = errorMessage + errorMessage1

        if errorMessage2:
            errorMessage = errorMessage + " " + errorMessage2

        return errorMessage

    def NavigateToRegistrationPage(self):
        self.driver.find_element_by_css_selector("a[href='/register']").click()
        return RegistrationPage(self.driver)
