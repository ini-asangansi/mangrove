from selenium.webdriver.remote.webelement import WebElement

__author__ = 'kumarr'

class RadioButton (WebElement):

    def __init__(self, radioButttonWebElement ):
        super(RadioButton, self).__init__(radioButttonWebElement.parent, radioButttonWebElement.id)
        self.webElement = radioButttonWebElement

    def is_enabled(self):
        return self.webElement.is_enabled()

    def is_selected(self):
        return self.webElement.is_selected()

    def set_selected(self):
        return self.webElement.select()

    def radio_button_status(self):
        return self.webElement.is_enabled()


       


