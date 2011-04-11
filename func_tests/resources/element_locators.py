__author__ = 'ritesh'
from selenium.webdriver.common.by import By

# By default every locator should be CSS

LOCATOR = "locator"
BY = "by"

LOGIN_USERNAME_TB = {"locator":"username","by":By.NAME}






#Registration Page Locator

ORGANIZATION_NAME_TB = {"locator":"input[name=organization_name]","by":By.CSS_SELECTOR}
ORGANIZATION_SECTOR_DD = {"locator":"select[name='organization_sector']","by":By.CSS_SELECTOR}
ORGANIZATION_ADDRESS_LINE1_TB = {"locator":"input[name=organization_addressline1]","by":By.CSS_SELECTOR}
ORGANIZATION_ADDRESS_LINE2_TB = {"locator":"input[name=organization_addressline2]","by":By.CSS_SELECTOR}
ORGANIZATION_CITY_TB = {"locator":"input[name=organization_city]","by":By.CSS_SELECTOR}
ORGANIZATION_STATE_TB = {"locator":"input[name=organization_state]","by":By.CSS_SELECTOR}
ORGANIZATION_COUNTRY_TB = {"locator":"input[name=organization_country]","by":By.CSS_SELECTOR}
ORGANIZATION_ZIPCODE_TB = {"locator":"input[name=organization_zipcode]","by":By.CSS_SELECTOR}
ORGANIZATION_OFFICE_PHONE_TB = {"locator":"input[name=organization_office_phone]","by":By.CSS_SELECTOR}
ORGANIZATION_WEBSITE_TB = {"locator":"input[name=organization_website]","by":By.CSS_SELECTOR}
ORGANIZATION_TITLE_TB = {"locator":"input[name=title]","by":By.CSS_SELECTOR}
ORGANIZATION_FIRST_NAME_TB = {"locator":"input[name=first_name]","by":By.CSS_SELECTOR}
ORGANIZATION_LAST_NAME_TB = {"locator":"input[name=last_name]","by":By.CSS_SELECTOR}
ORGANIZATION_EMAIL_TB = {"locator":"input[name=email]","by":By.CSS_SELECTOR}
ORGANIZATION_PASSWORD_TB = {"locator":"input[name=password]","by":By.CSS_SELECTOR}
ORGANIZATION_CONFIRM_PASSWORD_TB = {"locator":"input[name=confirm_password]","by":By.CSS_SELECTOR}
ORGANIZATION_REGISTER_B = {"locator":"input[value=Register]","by":By.CSS_SELECTOR}


#Successfull Registration Page Locator

WELCOME_MESSAGE_TB = {"locator":"div[class^=success]","by":By.CSS_SELECTOR}