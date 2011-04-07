from framework.utils.drop_down_web_element import DropDown
from framework.utils.text_box_web_element import TextBox
from framework.utils.radio_button_web_element import RadioButton

__author__ = 'anandb'

class DriverWrapper():

    def __init__(self):
        """Create DriverWrapper"""
        self.driver = self

    def find_drop_down(self, name):
        """ Finds the drop down using the driver.find_elements_by_name(...) api
        """
        return DropDown(self.find_element_by_name(name))

    def find_text_box(self, name):
        """ Finds a Text Box down using the driver.find_elements_by_name(...) api
        """
        return TextBox(self.find_element_by_name(name))

    def find_radio_button(self, id):
        """ Finds the Radio Button using the driver.find_elements_by_name(...) api
        """
        return RadioButton(self.find_element_by_id(id))
