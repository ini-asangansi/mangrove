# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

__author__ = 'ritesh'

USERNAME = 'username'
PASSWORD = 'password'
WELCOME_MESSAGE = 'message'
ERROR_MESSAGE = 'message'

# valid credentials
VALID_CREDENTIALS={"username":"nogo@mail.com","password":"nogo123",
                       "message":"Welcome Mr. No Go"}
# invalid email id
INVALID_EMAIL_ID_FORMAT={"username":"nogo@mail","password":"nogo123",
                       "message":"Your username and password didn't match. Please try again"}
# invalid password
INVALID_PASSWORD={"username":"nogo@mail.com","password":"nogo124",
                  "message":"Your username and password didn't match. Please try again"}

# blank username and password
BLANK_CREDENTIALS={"username":"","password":"",
                   "message":"Email: This field is required. Password: This field is required."}