# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
import logging

logging.getLogger('selenium.webdriver.firefox.utils').setLevel(logging.ERROR)
logging.getLogger('selenium.webdriver.firefox.firefox_profile').setLevel(logging.ERROR)
logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(logging.ERROR)
logging.getLogger('webdriver.ExtensionConnection').setLevel(logging.ERROR)
logging.getLogger('selenium.webdriver.firefox.firefoxlauncher').setLevel(logging.ERROR)
