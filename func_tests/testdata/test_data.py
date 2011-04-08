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