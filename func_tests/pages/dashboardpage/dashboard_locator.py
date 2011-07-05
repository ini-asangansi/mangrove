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

WELCOME_MESSAGE_LABEL = by_css("span.welcome")
REGISTER_REPORTER_LINK = by_css("a[href='/reporter/register']")
CREATE_PROJECT_LINK = by_css("a[href='/project/profile/create']")
REGISTER_SUBJECT_LINK = by_css("a[href='/admin/register/entity']")
VIEW_ALL_PROJECT_LINK = by_css("a[href='/project/']")
