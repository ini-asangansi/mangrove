# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

#Registration Page Test Data

##Variables
ORGANIZATION_NAME= 'organization_name'
ORGANIZATION_SECTOR = 'organization_sector'
ORGANIZATION_ADDRESS_LINE1 = 'organization_addressline1'
ORGANIZATION_ADDRESS_LINE2 = 'organization_addressline12'
ORGANIZATION_CITY= 'organization_city'
ORGANIZATION_STATE= 'organization_state'
ORGANIZATION_COUNTRY= 'organization_country'
ORGANIZATION_ZIPCODE= 'organization_zipcode'
ORGANIZATION_OFFICE_PHONE= 'organization_office_phone'
ORGANIZATION_WEBSITE= 'organization_website'
TITLE = 'title'
FIRST_NAME = 'first_name'
LAST_NAME = 'last_name'
EMAIL = 'email'
REGISTRATION_PASSWORD = 'registration_password'
REGISTRATION_CONFIRM_PASSWORD = 'registration_confirm_password'
SUCCESS_MESSAGE = 'message'
ERROR_MESSAGE = 'message'


#Registration Page Data for Successful Registration Page
REGISTRATION_DATA_FOR_SUCCESSFUL_REGISTRATION = {"organization_name":"NGO 001",
                                                "organization_sector":"PublicHealth",
                                                "organization_addressline1":"Address Line One",
                                                "organization_addressline2":"Address Line Two",
                                                "organization_city":"Pune",
                                                "organization_state":"Maharashtra",
                                                "organization_country":"India",
                                                "organization_zipcode":"411028",
                                                "organization_office_phone":"0123456789",
                                                "organization_website":"http://ngo001.com",
                                                "title":"Mr",
                                                "first_name":"No",
                                                "last_name":"Go",
                                                "email":"ngo001@ngo.com",
                                                "registration_password":"ngo001",
                                                "registration_confirm_password":"ngo001",
                                                "message":"You have successfully registered!! An activation email has been sent to your email address. Please activate before login."}

EXISTING_EMAIL_ADDRESS = {"organization_name":"NGO 001",
                                                "organization_sector":"PublicHealth",
                                                "organization_addressline1":"Address Line One",
                                                "organization_addressline2":"Address Line Two",
                                                "organization_city":"Pune",
                                                "organization_state":"Maharashtra",
                                                "organization_country":"India",
                                                "organization_zipcode":"411028",
                                                "organization_office_phone":"0123456789",
                                                "organization_website":"http://ngo001.com",
                                                "title":"Mr",
                                                "first_name":"No",
                                                "last_name":"Go",
                                                 "email":"tester150411@gmail.com",
                                                 "registration_password":"ngo001",
                                                 "registration_confirm_password":"ngo001",
                                                 "message":"Email address  This email address is already in use. Please supply a different email address."}

INVALID_EMAIL_FORMAT = {"organization_name":"NGO 001",
                                                "organization_sector":"PublicHealth",
                                                "organization_addressline1":"Address Line One",
                                                "organization_addressline2":"Address Line Two",
                                                "organization_city":"Pune",
                                                "organization_state":"Maharashtra",
                                                "organization_country":"India",
                                                "organization_zipcode":"411028",
                                                "organization_office_phone":"0123456789",
                                                "organization_website":"http://ngo001.com",
                                                "title":"Mr",
                                                "first_name":"No",
                                                "last_name":"Go",
                                                "email":"com.invalid@email",
                                                 "registration_password":"ngo001",
                                                 "registration_confirm_password":"ngo001",
                                                 "message":"Email address  Enter a valid e-mail address."}

UNMATCHED_PASSWORD = {"organization_name":"NGO 001",
                                                "organization_sector":"PublicHealth",
                                                "organization_addressline1":"Address Line One",
                                                "organization_addressline2":"Address Line Two",
                                                "organization_city":"Pune",
                                                "organization_state":"Maharashtra",
                                                "organization_country":"India",
                                                "organization_zipcode":"411028",
                                                "organization_office_phone":"0123456789",
                                                "organization_website":"http://ngo001.com",
                                                "title":"Mr",
                                                "first_name":"No",
                                                "last_name":"Go",
                                                "email":"valid@email.com",
                                                "registration_password":"password",
                                                "registration_confirm_password":"different_password",
                                                "message":"Password  The two password fields didn't match."}

WITHOUT_ENTERING_REQUIRED_FIELDS = {"organization_name":"",
                                                "organization_sector":"PublicHealth",
                                                "organization_addressline1":"",
                                                "organization_addressline2":"",
                                                "organization_city":"",
                                                "organization_state":"",
                                                "organization_country":"",
                                                "organization_zipcode":"",
                                                "organization_office_phone":"",
                                                "organization_website":"",
                                                "title":"",
                                                "first_name":"",
                                                "last_name":"",
                                                "email":"",
                                                "registration_password":"",
                                                "registration_confirm_password":"",
                                                "message":"* Organization name   This field is required.* Address Line 1  This field is required.* City  This field is required.* Country  This field is required.* Postal / Zip Code  This field is required.* First name  This field is required.* Last name  This field is required.Email address  This field is required.Password  This field is required.Password (again)  This field is required."}

INVALID_WEBSITE_URL = {"organization_name":"NGO 001",
                                                "organization_sector":"PublicHealth",
                                                "organization_addressline1":"Address Line One",
                                                "organization_addressline2":"Address Line Two",
                                                "organization_city":"Pune",
                                                "organization_state":"Maharashtra",
                                                "organization_country":"India",
                                                "organization_zipcode":"411028",
                                                "organization_office_phone":"0123456789",
                                                "organization_website":"ngo001",
                                                "title":"Mr",
                                                "first_name":"No",
                                                "last_name":"Go",
                                                "email":"ngo002@ngo.com",
                                                "registration_password":"ngo001",
                                                "registration_confirm_password":"ngo001",
                                                "message":"Website Url  Enter a valid URL."}