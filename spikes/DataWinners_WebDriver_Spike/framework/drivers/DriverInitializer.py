from framework.drivers.FirefoxDriverWrapper import FirefoxDriverWrapper
from framework.drivers.IEDriverWrapper import IEDriverWrapper
from framework.drivers.ChromeDriverWrapper import ChromeDriverWrapper
from framework.drivers.RemoteDriverWrapper import RemoteDriverWrapper

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

  