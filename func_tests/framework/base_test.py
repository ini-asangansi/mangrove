from framework.drivers.driver_initializer import DriverInitializer
from framework.mangrovetests.dashboard_page import DashboardPage

__author__ = 'anandb'


class BaseTest(object):
    def setup(self):
        self.driver = DriverInitializer.initialize ("firefox")

    def teardown(self):
        self.driver.quit()