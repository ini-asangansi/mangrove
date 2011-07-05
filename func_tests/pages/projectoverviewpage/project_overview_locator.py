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
# LABEL - Label


# variable to access locators
LOCATOR = "locator"
BY = "by"

DATA_TAB = by_xpath("//div[contains(@class,'tab_navigation')]/ul/li/a[text()='Data']")
PROJECT_EDIT_LINK = by_css("a[href~='/project/profile/edit']")
