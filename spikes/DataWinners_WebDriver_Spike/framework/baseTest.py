from framework.drivers.driver_initializer import DriverInitializer

__author__ = 'anandb'

import unittest

class BaseTest (unittest.TestCase):
    def setUp(self):
        self.driver = DriverInitializer.initialize ("chrome")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()

  