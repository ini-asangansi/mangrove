from selenium.webdriver.firefox.webdriver import WebDriver
from framework.drivers.driver_wrapper import DriverWrapper

__author__ = 'anandb'

class FirefoxDriverWrapper(WebDriver, DriverWrapper):
    def __init__(self):
        """ Create Firefox Driver Wrapper"""
        WebDriver.__init__(self)
        DriverWrapper.__init__(self)

