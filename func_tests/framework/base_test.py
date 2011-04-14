# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from framework.drivers.driver_initializer import DriverInitializer


class BaseTest(object):
    def setup(self):
        self.driver = DriverInitializer.initialize ("firefox")

    def teardown(self):
        self.driver.quit()