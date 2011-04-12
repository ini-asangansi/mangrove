# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from framework.drivers.driver_initializer import DriverInitializer
from framework.pages.dashboard_page import DashboardPage

__author__ = 'anandb'


class BaseTest(object):
    def setup(self):
        self.driver = DriverInitializer.initialize ("firefox")

    def teardown(self):
        self.driver.quit()