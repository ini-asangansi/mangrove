# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

__author__ = 'ritesh'

USERNAME = 'username'
PASSWORD = 'password'
WELCOME_MESSAGE = 'message'
ERROR_MESSAGE = 'message'

# valid credentials
VALID_CREDENTIALS={"username":"nogo@mail.com","password":"nogo123",
                       "message":"Welcome Mr. No Go"}
# invalid format email id
INVALID_EMAIL_ID_FORMAT={"username":"com.invalid@mail","password":"nogo123",
                       "message":"Please enter a correct username and password."}
# invalid password
INVALID_PASSWORD={"username":"nogo@mail.com","password":"nogo124",
                  "message":"Please enter a correct username and password."}

# Login without entering Email Address
BLANK_EMAIL_ADDRESS={"username":"","password":"nogo123",
                     "message":"This field is required."}

BLANK_PASSWORD={"username":"nogo@mail.com","password":"",
                "message":"This field is required."}


# blank username and password
UNACTIVATED_ACCOUNT_CREDENTIALS={"username":"nogo@mail.com","password":"nogo123",
                   "message":"This account is inactive."}


# blank username and password
BLANK_CREDENTIALS={"username":"","password":"",
                   "message":"This field is required.This field is required."}
