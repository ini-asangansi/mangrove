# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8


USERNAME = 'username'
PASSWORD = 'password'
WELCOME_MESSAGE = 'message'
ERROR_MESSAGE = 'message'

# valid credentials
VALID_CREDENTIALS = {"username": "tester150411@gmail.com",
                   "password": "tester150411",
                       "message": "Welcome Mr. Tester Pune"}
# invalid format email id
INVALID_EMAIL_ID_FORMAT = {"username": "com.invalid@mail",
                           "password": "nogo123",
                       "message": "Please enter a correct email and password."}
# invalid password
INVALID_PASSWORD = {"username": "nogo@mail.com", "password": "nogo124",
                  "message": "Please enter a correct email and password."}

# Login without entering Email Address
BLANK_EMAIL_ADDRESS = {"username": "", "password": "nogo123",
                     "message": "Email  This field is required."}

BLANK_PASSWORD = {"username": "nogo@mail.com", "password": "",
                "message": "Password  This field is required."}


# blank username and password
UNACTIVATED_ACCOUNT_CREDENTIALS = {"username": "tester@gmail.com",
                                 "password": "nogo123",
                   "message": "This account is inactive."}


# blank username and password
BLANK_CREDENTIALS = {"username": "", "password": "",
                   "message": "Email  This field is required.Password  This field is required."}
