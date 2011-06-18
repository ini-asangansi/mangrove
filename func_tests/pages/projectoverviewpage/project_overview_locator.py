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

VIEW_SUBMISSIONS_CLICK_HERE_LINK = by_xpath("//h5[text()='View Submissions']/following-sibling::p/a[text()='Click here']")
PROJECT_EDIT_LINK = by_css("a[href~='/project/profile/edit']")
