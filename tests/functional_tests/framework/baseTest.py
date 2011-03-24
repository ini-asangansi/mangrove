from framework.drivers.DriverInitializer import DriverInitializer

__author__ = 'anandb'

import unittest

class BaseTest (unittest.TestCase):
    def setUp(self):
        self.driver = DriverInitializer.initialize ("firefox")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()

  