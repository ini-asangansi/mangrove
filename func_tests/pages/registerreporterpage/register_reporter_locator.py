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

FIRST_NAME_TB = by_css("input#id_first_name")
LAST_NAME_TB = by_css("input#id_last_name")
TELEPHONE_NUMBER_TB = by_css("input#id_telephone_number")
COMMUNE_TB = by_css("input#id_commune")

REGISTER_BTN = by_css("input[value='Register']")
ERROR_MESSAGE_LABEL = by_css("div[class~='error']")
FLASH_MESSAGE_LABEL = by_xpath("//div[@id='flash-message' and not(contains(@id, 'none'))]")