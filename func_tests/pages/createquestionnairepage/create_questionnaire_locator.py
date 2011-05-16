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
QUESTION_TB = by_xpath("//input[@id='question']")
CODE_TB = by_css("input#code")
WORD_OR_PHRASE_RB = by_css("input[value='text']")
WORD_OR_PHRASE_MIN_LENGTH_TB = by_xpath("//li[not(contains(@style,'none')) and contains(@data-bind,'showAddTextLength')]/div/p/input[@id='min_length']")
WORD_OR_PHRASE_MAX_LENGTH_TB = by_xpath("//li[not(contains(@style,'none')) and contains(@data-bind,'showAddTextLength')]/div/p/input[@id='max_length']")
NUMBER_RB = by_css("input[value='integer']")
NUMBER_MAX_LENGTH_TB = by_xpath("//li[not(contains(@style,'none')) and contains(@data-bind,'showAddRange')]/div/p/input[@id='range_max']")
NUMBER_MIN_LENGTH_TB = by_xpath("//li[not(contains(@style,'none')) and contains(@data-bind,'showAddRange')]/div/p/input[@id='range_min']")

DATE_RB = by_css("input[value='date']")
MONTH_YEAR_RB = by_css("input[value='%m.%Y']")
DATE_MONTH_YEAR_RB = by_css("input[value='%d.%m.%Y']")
MONTH_DATE_YEAR_RB = by_css("input[value='%m.%d.%Y']")

LIST_OF_CHOICE_RB = by_css("input[value='choice']")
CHOICE_XPATH_LOCATOR = "//li[not(contains(@style,'none')) and contains(@data-bind,'showAddChoice')]/div/div/p"
CHOICE_TB_XPATH_LOCATOR = "/input"
CHOICE_DELETE_LINK_XPATH_LOCATOR = "/a[text()='delete']"
ADD_CHOICE_LINK = by_xpath("//li[not(contains(@style,'none')) and contains(@data-bind,'showAddChoice')]/div/a")
ONLY_ONE_ANSWER_RB = by_css("input[value='select1']")
MULTIPLE_ANSWER_RB = by_css("input[value='select']")

# Locators for Question List section of the page
DEFAULT_QUESTION_LINK = by_xpath("//div[@class='question_list']/ol/li/a[contains(text(),'What are you reporting on')]")
QUESTION_LINK_CSS_LOCATOR = "div.question_list>ol>li>a"  # Add text or index number to identify question
QUESTION_DELETE_LINK_CSS_LOCATOR_PART1 = "div.question_list>ol>li>a:contains('"  # Add text or index number to identify question
QUESTION_DELETE_LINK_CSS_LOCATOR_PART1 = "')~div>span.delete>a"
ADD_A_QUESTION_LINK = by_css("div.add_question>a")
SAVE_CHANGES_BTN = by_css("input#submit-button")

SUCCESS_MESSAGE_LABEL = by_xpath("//div[@id='message-label']/label[@class='success_message' and not(contains(@style,'none'))]")