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

QUESTIONNAIRE_CODE_TB = by_css("input#questionnaire-code")
QUESTION_TB = by_css("input#question")
CODE_TB = by_css("input#code")
WORD_OR_PHRASE_RB = by_css("input[value='text']")
NUMBER_RB = by_css("input[value='integer']")
DATE_RB = by_css("input[value='date']")
LIST_OF_CHOICE_RB = by_css("input[value='choice']")
MONTH_YEAR_RB = by_css("input[value='%m.%Y']")
DATE_MONTH_YEAR_RB = by_css("input[value='%d.%m.%Y']")
MONTH_DATE_YEAR_RB = by_css("input[value='%m.%d.%Y']")
ADD_CHOICE_LINK = by_css("a:contains('Add Choice')")
ONLY_ONE_ANSWER_RB = by_css("input[value='select1']")
MULTIPLE_ANSWER_RB = by_css("input[value='select']")

SMS_CB = by_css("input[value='sms']")
SMART_PHONE_CB = by_css("input[value='smartphone']")
WEB_CB = by_css("input[value='web']")
SAVE_CHANGES_BTN = by_css("input#submit-button")
PROJECT_NAME_ERROR_MSG_LABEL = by_css("li>input#id_name~ul.errorlist>li")
PROJECT_TYPE_ERROR_MSG_LABEL = by_css("li>label[for='id_project_type_0']~ul.errorlist>li")
ADD_QUESTION_LINK = by_css("a:contains('Add a Question')")