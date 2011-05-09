# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from selenium.webdriver.common.by import By

from pages.page import Page
from pages.dashboardpage.dashboard_page import DashboardPage
from pages.registrationpage.registration_page import  RegistrationPage
from framework.utils.common_utils import CommonUtilities
from framework.utils.data_fetcher import *
from pages.loginpage.login_locator import *
from tests.logintests.login_data import *


class LoginPage(Page):

    def __init__(self, driver):
        Page.__init__(self, driver)

    def do_successful_login_with(self, login_credential):
        """
        Function to login into the website with valid credentials

        Args:
        'login_credential' is valid login credentials of the user

        Return DashboardPage on successful login
        """
        self.driver.find_text_box(EMAIL_TB).enter_text(fetch_(USERNAME, from_(login_credential)))
        self.driver.find_text_box(PASSWORD_TB).enter_text(fetch_(PASSWORD, from_(login_credential)))
        self.driver.find(LOGIN_BTN).click()
        return DashboardPage(self.driver)

    def login_with(self, login_credential):
        """
        Function to enter email id and password in the text boxes and click
        on the login button. This function is used for testing error messages
         only
         .
        Args:
        'login_credential' is login credentials of the user e.g. email and password

        Return LoginPage 
        """
        self.driver.find_text_box(EMAIL_TB).enter_text(fetch_(USERNAME, from_(login_credential)))
        self.driver.find_text_box(PASSWORD_TB).enter_text(fetch_(PASSWORD, from_(login_credential)))
        self.driver.find(LOGIN_BTN).click()
        return self

    def get_error_message(self):
        """
        Function to fetch the error messages from error label of the login
        page

        Return error message
        """
        error_message = ""
        locators = self.driver.find_elements_(ERROR_MESSAGE_LABEL)
        if locators:
            for locator in locators:
                error_message = error_message + locator.text
        return error_message.replace("\n", " ")

    def navigate_to_registration_page(self):
        """
        Function to click on register page link which is available on the login page

        Return RegistrationPage
        """
        self.driver.find_element_by_css_selector("a[href='/register']").click()
        return RegistrationPage(self.driver)
