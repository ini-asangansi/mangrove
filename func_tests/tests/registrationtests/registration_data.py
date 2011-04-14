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
                                                 "registration_confirm_password":"ngo001"}

REGISTRATION_DATA_FOR_EXISTING_EMAIL_ERROR = {"organization_name":"NGO 001",
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
                                                 "email":"nogo@mail.com",
                                                 "registration_password":"ngo001",
                                                 "registration_confirm_password":"ngo001"}

REGISTRATION_DATA_FOR_INVALID_FORMAT_EMAIL_ERROR = {"organization_name":"NGO 001",
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
                                                 "registration_confirm_password":"ngo001"}

REGISTRATION_DATA_FOR_UNMATCHED_PASSWORD = {"organization_name":"NGO 001",
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
                                                "registration_confirm_password":"different_password"}