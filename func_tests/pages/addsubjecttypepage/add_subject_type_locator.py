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

# List of all the locators related to login page
NEW_SUBJECT_TB = by_css("input#id_entity_type")
ADD_BTN = by_css("input[value='Add']")

ERROR_MESSAGE_LABEL = by_css("ul.errorlist>li")
FLASH_MESSAGE_LABEL = by_xpath("//div[@id='flash-message' and not(contains(@style,'none'))]")
