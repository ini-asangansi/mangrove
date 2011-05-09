# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

#Registration Page Test Data

##Variables
ORGANIZATION_NAME = 'organization_name'
ORGANIZATION_SECTOR = 'organization_sector'
ORGANIZATION_ADDRESS_LINE1 = 'organization_addressline1'
ORGANIZATION_ADDRESS_LINE2 = 'organization_addressline12'
ORGANIZATION_CITY = 'organization_city'
ORGANIZATION_STATE = 'organization_state'
ORGANIZATION_COUNTRY = 'organization_country'
ORGANIZATION_ZIPCODE = 'organization_zipcode'
ORGANIZATION_OFFICE_PHONE = 'organization_office_phone'
ORGANIZATION_WEBSITE = 'organization_website'
TITLE = 'title'
FIRST_NAME = 'first_name'
LAST_NAME = 'last_name'
EMAIL = 'email'
REGISTRATION_PASSWORD = 'registration_password'
REGISTRATION_CONFIRM_PASSWORD = 'registration_confirm_password'
SUCCESS_MESSAGE = 'message'
ERROR_MESSAGE = 'message'


#Registration Page Data for Successful Registration Page
REGISTRATION_DATA_FOR_SUCCESSFUL_REGISTRATION = {ORGANIZATION_NAME: "NGO 001",
                       ORGANIZATION_SECTOR: "PublicHealth",
                       ORGANIZATION_ADDRESS_LINE1: "Address Line One",
                       ORGANIZATION_ADDRESS_LINE2: "Address Line Two",
                       ORGANIZATION_CITY: "Pune",
                       ORGANIZATION_STATE: "Maharashtra",
                       ORGANIZATION_COUNTRY: "India",
                       ORGANIZATION_ZIPCODE: "411028",
                       ORGANIZATION_OFFICE_PHONE: "0123456789",
                       ORGANIZATION_WEBSITE: "http://ngo001.com",
                       TITLE: "Mr",
                       FIRST_NAME: "No",
                       LAST_NAME: "Go",
                       EMAIL: "ngo001@ngo.com",
                       REGISTRATION_PASSWORD: "ngo001",
                       REGISTRATION_CONFIRM_PASSWORD: "ngo001",
                       SUCCESS_MESSAGE: "You have successfully registered!! An activation email has been sent to your email address. Please activate before login."}

EXISTING_EMAIL_ADDRESS = {ORGANIZATION_NAME: "NGO 001",
                       ORGANIZATION_SECTOR: "PublicHealth",
                       ORGANIZATION_ADDRESS_LINE1: "Address Line One",
                       ORGANIZATION_ADDRESS_LINE2: "Address Line Two",
                       ORGANIZATION_CITY: "Pune",
                       ORGANIZATION_STATE: "Maharashtra",
                       ORGANIZATION_COUNTRY: "India",
                       ORGANIZATION_ZIPCODE: "411028",
                       ORGANIZATION_OFFICE_PHONE: "0123456789",
                       ORGANIZATION_WEBSITE: "http://ngo001.com",
                       TITLE: "Mr",
                       FIRST_NAME: "No",
                       LAST_NAME: "Go",
                        EMAIL: "tester150411@gmail.com",
                        REGISTRATION_PASSWORD: "ngo001",
                        REGISTRATION_CONFIRM_PASSWORD: "ngo001",
                        ERROR_MESSAGE: "Email address  This email address is already in use. Please supply a different email address."}

INVALID_EMAIL_FORMAT = {ORGANIZATION_NAME: "NGO 001",
                        ORGANIZATION_SECTOR: "PublicHealth",
                        ORGANIZATION_ADDRESS_LINE1: "Address Line One",
                        ORGANIZATION_ADDRESS_LINE2: "Address Line Two",
                        ORGANIZATION_CITY: "Pune",
                        ORGANIZATION_STATE: "Maharashtra",
                        ORGANIZATION_COUNTRY: "India",
                        ORGANIZATION_ZIPCODE: "411028",
                        ORGANIZATION_OFFICE_PHONE: "0123456789",
                        ORGANIZATION_WEBSITE: "http://ngo001.com",
                        TITLE: "Mr",
                        FIRST_NAME: "No",
                        LAST_NAME: "Go",
                        EMAIL: "com.invalid@email",
                        REGISTRATION_PASSWORD: "ngo001",
                        REGISTRATION_CONFIRM_PASSWORD: "ngo001",
                        ERROR_MESSAGE: "Email address  Enter a valid e-mail address."}

UNMATCHED_PASSWORD = {ORGANIZATION_NAME: "NGO 001",
                       ORGANIZATION_SECTOR: "PublicHealth",
                       ORGANIZATION_ADDRESS_LINE1: "Address Line One",
                       ORGANIZATION_ADDRESS_LINE2: "Address Line Two",
                       ORGANIZATION_CITY: "Pune",
                       ORGANIZATION_STATE: "Maharashtra",
                       ORGANIZATION_COUNTRY: "India",
                       ORGANIZATION_ZIPCODE: "411028",
                       ORGANIZATION_OFFICE_PHONE: "0123456789",
                       ORGANIZATION_WEBSITE: "http://ngo001.com",
                       TITLE: "Mr",
                       FIRST_NAME: "No",
                       LAST_NAME: "Go",
                       EMAIL: "valid@email.com",
                       REGISTRATION_PASSWORD: "password",
                       REGISTRATION_CONFIRM_PASSWORD: "different_password",
                       ERROR_MESSAGE: "Password  The two password fields didn't match."}

WITHOUT_ENTERING_REQUIRED_FIELDS = {ORGANIZATION_NAME: "",
                       ORGANIZATION_SECTOR: "PublicHealth",
                       ORGANIZATION_ADDRESS_LINE1: "",
                       ORGANIZATION_ADDRESS_LINE2: "",
                       ORGANIZATION_CITY: "",
                       ORGANIZATION_STATE: "",
                       ORGANIZATION_COUNTRY: "",
                       ORGANIZATION_ZIPCODE: "",
                       ORGANIZATION_OFFICE_PHONE: "",
                       ORGANIZATION_WEBSITE: "",
                       TITLE: "",
                       FIRST_NAME: "",
                       LAST_NAME: "",
                       EMAIL: "",
                       REGISTRATION_PASSWORD: "",
                       REGISTRATION_CONFIRM_PASSWORD: "",
                       ERROR_MESSAGE: "* Organization name   This field is required.* Address Line 1  This field is required.* City  This field is required.* Country  This field is required.* Postal / Zip Code  This field is required.* First name  This field is required.* Last name  This field is required.Email address  This field is required.Password  This field is required.Password (again)  This field is required."}

INVALID_WEBSITE_URL = {ORGANIZATION_NAME: "NGO 001",
                       ORGANIZATION_SECTOR: "PublicHealth",
                       ORGANIZATION_ADDRESS_LINE1: "Address Line One",
                       ORGANIZATION_ADDRESS_LINE2: "Address Line Two",
                       ORGANIZATION_CITY: "Pune",
                       ORGANIZATION_STATE: "Maharashtra",
                       ORGANIZATION_COUNTRY: "India",
                       ORGANIZATION_ZIPCODE: "411028",
                       ORGANIZATION_OFFICE_PHONE: "0123456789",
                       ORGANIZATION_WEBSITE: "ngo001",
                       TITLE: "Mr",
                       FIRST_NAME: "No",
                       LAST_NAME: "Go",
                       EMAIL: "ngo002@ngo.com",
                       REGISTRATION_PASSWORD: "ngo001",
                       REGISTRATION_CONFIRM_PASSWORD: "ngo001",
                       ERROR_MESSAGE: "Website Url  Enter a valid URL."}
