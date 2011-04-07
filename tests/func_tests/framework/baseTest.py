from framework.drivers.DriverInitializer import DriverInitializer

__author__ = 'anandb'


class BaseTest(object):
    def setUp(self):
        self.driver = DriverInitializer.initialize ("firefox")

    def tearDown(self):
        self.driver.quit()