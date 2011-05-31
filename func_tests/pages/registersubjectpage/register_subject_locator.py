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


# variable to access locator
LOCATOR = "locator"
BY = "by"

ENTITY_TYPE_DD = by_name("type")
DROP_DOWN_OPTION_CSS = "select[name='type']>option[value='%s']"
SHORT_NAME_ENABLED_TB = by_css("input#short_name:enabled")
SHORT_NAME_DISABLED_TB = by_css("input#short_name:disabled")
AUTO_GENERATE_CB = by_css("input#autogen")
NAME_TB = by_name("name")
LOCATION_TB = by_name("location")
GEO_CODE_TB = by_name("geo_code")
DESCRIPTION_TB = by_name("description")
MOBILE_NUMBER_TB = by_name("mobile_number")

REGISTER_BTN = by_css("input#register_entity")
ERROR_MESSAGE_LABEL = by_xpath("//span/label[@class='error' and not(contains(@id,'none'))]/../..")
FLASH_MESSAGE_LABEL = by_xpath("//span[@id='message' and not(contains(@id,'none'))]")
