# vim: ai ts=4 sts=4 et sw=4utf-8
from nose.plugins.attrib import attr
from framework.base_test import BaseTest
from framework.utils.data_fetcher import from_, fetch_
from pages.loginpage.login_page import LoginPage
from nose.plugins.skip import SkipTest
from testdata.test_data import DATA_WINNER_LOGIN_PAGE
from tests.logintests.login_data import *


class TestIntregationOfApplication(BaseTest):
    @SkipTest
    @attr('functional_test', 'smoke')
    def test_intregation_of_application(self):
        self.driver.go_to(DATA_WINNER_LOGIN_PAGE)
        login_page = LoginPage(self.driver)

        dashboard_page = login_page.do_successful_login_with(VALID_CREDENTIALS)
        self.assertEqual(dashboard_page.welcome_message(),
            fetch_(WELCOME_MESSAGE, from_(VALID_CREDENTIALS)),
          "Login Un-successful or Welcome Message is not Present")
