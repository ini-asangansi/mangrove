

__author__ = 'ravi'

from framework.mangrovetests.page import Page
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import datetime

class CommonUtilities(Page):

    def __init__(self, driver):
        Page.__init__(self, driver)

    def wait_for_element(self, time_out_in_seconds, object_id):
        """Finds elements by their id by waiting till timeout."""

        current_time = datetime.datetime.now()
        end_time = current_time + datetime.timedelta(0,time_out_in_seconds)

        while current_time < end_time:
            try:
                self.driver.find_element_by_id(object_id)
                print "Object", object_id, "is present."
                break
            except NoSuchElementException:
                current_time = datetime.datetime.now()
        return self

    def find_text_box_by_id_and_enter_text(self, text_box_id, text_to_be_entered):
        self.driver.find_element_by_id(text_box_id).send_keys(text_to_be_entered)
        return self

    def find_text_box_by_name_and_enter_text(self, text_box_name, text_to_be_entered):
        self.driver.find_element_by_name(text_box_name).send_keys(text_to_be_entered)
        return self

    def find_text_box_by_css_and_enter_text(self, text_box_css, text_to_be_entered):
        self.driver.find_element_by_name(text_box_css).send_keys(text_to_be_entered)
        return self

    def find_drop_down_by_id_and_select_option(self, drop_down_id,
                                         option_to_be_selected):
        self.driver.find_drop_down(drop_down_id).set_selected(option_to_be_selected)
        return self

    def find_drop_down_by_name_and_select_option(self, drop_down_name,
                                         option_to_be_selected):
        self.driver.find_drop_down(drop_down_name).set_selected(option_to_be_selected)
        return self

    def find_element_and_click(self, element_id):
         self.driver.find_element_by_id(element_id).click()
         return self

    def is_element_present(self, element_locator, by=By.CSS_SELECTOR):
        try:
            locator = self.driver.find_element(by,element_locator)
            return locator
        except NoSuchElementException:
            return False
