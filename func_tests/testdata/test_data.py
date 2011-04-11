__author__ = 'root'

USERNAME='username'
PASSWORD='password'
MESSAGE='message'

# valid credentials
LOGIN_CREDENTIALS_ID1={"username":"nogo@mail.com","password":"nogo123",
                       "message":"Welcome Mr. No Go"}
# invalid email id
LOGIN_CREDENTIALS_ID2={"username":"nogo@mail","password":"nogo123",
                       "message":"Your username and password didn't match. Please try again"}
# invalid password
LOGIN_CREDENTIALS_ID3={"username":"nogo@mail.com","password":"nogo124"}

# blank username and password
LOGIN_CREDENTIALS_ID4={"username":"","password":""}





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
REGISTRATION_DATA_FOR_SUCCESSFUL_REGISTRATION ={"organization_name":"NGO 001",
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

REGISTRATION_DATA_FOR_EXISTING_EMAIL_ERROR ={"organization_name":"NGO 001",
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