# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8


from framework.utils.common_utils import *

# By default every locator should be CSS
# Abbr:
# TB - Text Box
# CB - Check Box
# RB - Radio Button
# BTN - Button
# DD - Drop Down
# LINK - Links


# variable to access locators
LOCATOR = "locator"
BY = "by"

# List of all the locators related to login page
EMAIL_TB = by_css("input[name=username]")
PASSWORD_TB = by_css("input[name=password]")
LOGIN_BTN = by_css("input[value=Login]")
