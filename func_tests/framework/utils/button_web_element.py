# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

__author__ = 'kumarr'

from selenium.webdriver.remote.webelement import WebElement

__author__ = 'anandb'

class Button (WebElement):

    def __init__(self, buttonWebElement ):
        super(Button, self).__init__(buttonWebElement.parent, buttonWebElement.id)
        self.webElement = buttonWebElement

    def enter_text(self, textToBeEntered):
        self.webElement.send_keys(textToBeEntered)
        return self

    def is_enabled(self):
        return self.webElement.is_enabled()
  