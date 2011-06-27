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

PROJECT_NAME_TB = by_css("input#id_name")
PROJECT_BACKGROUND_TB = by_css("textarea#id_goals")
SURVEY_PROJECT_RB = by_css("input[value='survey']")
PUBLIC_INFORMATION_RB = by_css("input[value='public information']")
DATA_SENDER_RB = by_css("input#id_activity_report_0")
OTHER_SUBJECT_RB = by_css("input#id_activity_report_1")
SUBJECTS_DD = by_css("select#id_entity_type")

SMS_CB = by_css("input[value='sms']")
SMS_CB_CHECKED = by_css("input[value='sms']:checked")
SMART_PHONE_CB = by_css("input[value='smartphone']")
SMART_PHONE_CB_CHECKED = by_css("input[value='smartphone']:checked")
WEB_CB = by_css("input[value='web']")
WEB_CB_CHECKED = by_css("input[value='web']:checked")
SAVE_CHANGES_BTN = by_css("input#submit-button")
PROJECT_NAME_ERROR_MSG_LABEL = by_css("li>input#id_name~ul.errorlist>li")
PROJECT_TYPE_ERROR_MSG_LABEL = by_css("li>label[for='id_project_type_0']~ul.errorlist>li")
QUESTIONNAIRE_ABOUT_MSG_LABEL = by_css("li>label[for='id_activity_report_0']~ul.errorlist>li")
