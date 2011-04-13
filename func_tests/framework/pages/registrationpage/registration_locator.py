# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

__author__ = 'ritesh'

from framework.utils.common_utils import *

# By default every locator should be CSS

LOCATOR = "locator"
BY = "by"

#Registration Page Locator
ORGANIZATION_NAME_TB = by_css("input[name=organization_name]")
ORGANIZATION_SECTOR_DD = by_css("select[name='organization_sector']")
ORGANIZATION_ADDRESS_LINE1_TB = by_css("input[name=organization_addressline1]")
ORGANIZATION_ADDRESS_LINE2_TB = by_css("input[name=organization_addressline2]")
ORGANIZATION_CITY_TB = by_css("input[name=organization_city]")
ORGANIZATION_STATE_TB = by_css("input[name=organization_state]")
ORGANIZATION_COUNTRY_TB = by_css("input[name=organization_country]")
ORGANIZATION_ZIPCODE_TB = by_css("input[name=organization_zipcode]")
ORGANIZATION_OFFICE_PHONE_TB = by_css("input[name=organization_office_phone]")
ORGANIZATION_WEBSITE_TB = by_css("input[name=organization_website]")
ORGANIZATION_TITLE_TB = by_css("input[name=title]")
ORGANIZATION_FIRST_NAME_TB = by_css("input[name=first_name]")
ORGANIZATION_LAST_NAME_TB = by_css("input[name=last_name]")
ORGANIZATION_EMAIL_TB = by_css("input[name=email]")
ORGANIZATION_PASSWORD_TB = by_css("input[name=password1]")
ORGANIZATION_CONFIRM_PASSWORD_TB = by_css("input[name=password2]")
ORGANIZATION_REGISTER_B = by_css("input[value=Register]")
  