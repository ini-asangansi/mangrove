from framework.drivers.driver_initializer import DriverInitializer

__author__ = 'anandb'


class BaseTest(object):
    def setup(self):
        self.driver = DriverInitializer.initialize ("firefox")

    def teardown(self):
        self.driver.quit()