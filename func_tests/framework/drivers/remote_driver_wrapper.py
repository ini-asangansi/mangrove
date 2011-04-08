from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from framework.drivers.driver_wrapper import DriverWrapper

__author__ = 'anandb'

class RemoteDriverWrapper(WebDriver, DriverWrapper):

    def __init__(self, timeout=30):
        """ Create htmlunit Driver Wrapper"""
        WebDriver.__init__(self,
            command_executor="http://127.0.0.1:4444/wd/hub",
            desired_capabilities= DesiredCapabilities.HTMLUNITWITHJS,
            browser_profile=None)

        DriverWrapper.__init__(self)
