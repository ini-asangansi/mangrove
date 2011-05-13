# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from framework.utils.drop_down_web_element import DropDown
from framework.utils.text_box_web_element import TextBox
from framework.utils.radio_button_web_element import RadioButton
from pages.loginpage.login_locator import *
from selenium.webdriver.common.exceptions import NoSuchElementException


class DriverWrapper():
    """
    DriverWrapper class is for creating an wrapper over traditional webdriver
     class. To do some additional function on different web elements
    """
    def __init__(self):
        """Create DriverWrapper"""
        self.driver = self

    def find_drop_down(self, locator_dict):
        """
        Create DropDown class object with the given web element

        Args:
        locator_dict is the dictionary of the locator which contains key
        values like {"locator":"input[name='email']","by":"By.CSS_SELECTOR"}

        Return DropDown
        """
        return DropDown(self.driver.find(locator_dict))

    def find_text_box(self, locator_dict):
        """
        Create TextBox class object with the given web element

        Args:
        locator_dict is the dictionary of the locator which contains key
        values like {"locator":"input[name='email']","by":"By.CSS_SELECTOR"}

        Return TextBox
        """
        return TextBox(self.driver.find(locator_dict))

    def find_radio_button(self, locator_dict):
        """
        Create RadioButton class object with the given web element

        Args:
        locator_dict is the dictionary of the locator which contains key
        values like {"locator":"input[name='email']","by":"By.CSS_SELECTOR"}

        Return RadioButton
        """
        return RadioButton(self.driver.find(locator_dict))

    def find(self, locator_dict):
        """
        Finds element on the web page using locator dictionary

        Args:
        locator_dict is the dictionary of the locator which contains key
        values like {"locator":"input[name='email']","by":"By.CSS_SELECTOR"}

        Return webelement
        """
        try:
            return self.driver.find_element(by=locator_dict[BY],
                                        value=locator_dict[LOCATOR])
        except NoSuchElementException as e:
            raise e


    def find_elements_(self, locator_dict):
        """
        Finds elements on the web page using locator dictionary

        Args:
        locator_dict is the dictionary of the locator which contains key
        values like {"locator":"input[name='email']","by":"By.CSS_SELECTOR"}

        Return list of webelement
        """
        return self.driver.find_elements(by=locator_dict[BY],
                                        value=locator_dict[LOCATOR])

    def go_to(self, url):
        """
        Open URL using get command of webdriver api

        Args:
        url is url of the website
        """
        self.driver.get(url)
