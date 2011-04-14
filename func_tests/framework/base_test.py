# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from framework.drivers.driver_initializer import DriverInitializer
import unittest

class BaseTest(unittest.TestCase):
    def setUp(self):
        self.driver = DriverInitializer.initialize ("htmlunit")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()