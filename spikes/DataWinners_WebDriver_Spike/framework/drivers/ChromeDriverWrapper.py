__author__ = 'kumarr'


from selenium.webdriver.chrome.webdriver import WebDriver
from framework.drivers.DriverWrapper import DriverWrapper

class ChromeDriverWrapper(WebDriver, DriverWrapper):
    def __init__(self):
        """ Create Chrome Driver Wrapper"""
        WebDriver.__init__(self)
        DriverWrapper.__init__(self)