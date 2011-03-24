from selenium.webdriver.ie.webdriver import WebDriver
from framework.drivers.DriverWrapper import DriverWrapper

__author__ = 'anandb'

class IEDriverWrapper(WebDriver, DriverWrapper):
    def __init__(self):
        """ Create IE Driver Wrapper"""
        WebDriver.__init__(self)
        DriverWrapper.__init__(self)
