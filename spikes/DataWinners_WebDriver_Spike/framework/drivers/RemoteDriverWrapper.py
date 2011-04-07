from selenium.webdriver.remote.webdriver import WebDriver
from framework.drivers.driver_wrapper import DriverWrapper

__author__ = 'anandb'

class RemoteDriverWrapper(WebDriver, DriverWrapper):
    def __init__(self, timeout=30):
        """ Create htmlunit Driver Wrapper"""
        WebDriver.__init__(self,
            command_executor="http://localhost:4444/wd/hub",
            browser_name='htmlunit', platform='ANY', version='',
            javascript_enabled=True)

        DriverWrapper.__init__(self)
