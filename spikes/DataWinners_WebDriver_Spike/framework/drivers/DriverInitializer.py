from framework.drivers.firefox_driver_wrapper import FirefoxDriverWrapper
from framework.drivers.ie_driver_wrapper import IEDriverWrapper
from framework.drivers.chrome_driver_wrapper import ChromeDriverWrapper
from framework.drivers.remote_driver_wrapper import RemoteDriverWrapper

__author__ = 'anandb'

class DriverInitializer:
    @classmethod
    def initialize(self, browser):
        """ Create Driver Wrapper"""
        print "Creating %s wrapper" % browser
        if browser == "firefox":
            self.wrapper = FirefoxDriverWrapper()
        elif browser == "ie":
            self.wrapper = IEDriverWrapper()
        elif browser == "chrome":
            self.wrapper = ChromeDriverWrapper()
        elif browser == "htmlunit":
            self.wrapper = RemoteDriverWrapper()
        return self.wrapper.driver

  