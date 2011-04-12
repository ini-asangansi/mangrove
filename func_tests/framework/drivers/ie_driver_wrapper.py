# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from selenium.webdriver.ie.webdriver import WebDriver
from framework.drivers.driver_wrapper import DriverWrapper

__author__ = 'anandb'

class IEDriverWrapper(WebDriver, DriverWrapper):
    def __init__(self):
        """ Create IE Driver Wrapper"""
        WebDriver.__init__(self)
        DriverWrapper.__init__(self)
