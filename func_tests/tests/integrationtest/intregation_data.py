# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

WELCOME_MESSAGE = 'message'
SUCCESS_MESSAGE = 'message'
ERROR_MESSAGE = 'message'

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

ACTIVATION_CODE = "activation_code"

USERNAME = 'username'
PASSWORD = 'password'

REPORTER_NAME = "name"
TELEPHONE_NUMBER = "telephone_number"
COMMUNE = "commune"
GPS = "gps"

ENTITY_TYPE = "entity_type"
SHORT_NAME = "short_name"
AUTO_GENERATE = "auto_generate"
NAME = "name"
LOCATION = "location"
GEO_CODE = "geo_code"
MOBILE_NUMBER = "mobile_number"
DESCRIPTION = "description"

PROJECT_NAME = "project_name"
PROJECT_BACKGROUND = "project_background"
PROJECT_TYPE = "project_type"
SUBJECT = "subject"
DEVICES = "devices"
ERROR_MSG = "message"
PAGE_TITLE = "page_title"
GEN_RANDOM = "gen_random"

QUESTIONNAIRE_CODE = "questionnaire_code"
GEN_RANDOM = "gen_random"
DEFAULT_QUESTION = "default_question"
QUESTION = "question"
QUESTIONS = "questions"
CODE = "code"
TYPE = "type"
LIMIT = "limit"
NO_LIMIT = "no_limit"
LIMITED = "limited"
MIN = "min"
MAX = "max"
DATE_FORMAT = "date_format"
CHOICE = "choice"
ALLOWED_CHOICE = "allowed_choice"
NUMBER = "number"
WORD = "word"
DATE = "date"
LIST_OF_CHOICES = "list_of_choices"
GEO = "geo"
DD_MM_YYYY = "dd.mm.yyyy"
MM_DD_YYYY = "mm.dd.yyyy"
MM_YYYY = "mm.yyyy"
ONLY_ONE_ANSWER = "only_one_answer"
MULTIPLE_ANSWERS = "multiple_answers"
CHARACTER_REMAINING = "character_remaining"

SENDER = "to"
RECEIVER = "from"
SMS = "sms"
MESSAGE = "message"

SUCCESS_MESSAGE_TEXT = "Thank you Donald Mouse. We received : WAN: Mr. Tessy WID: wel1 WC: DARK YELLOW WB: Aquificae,Bacteroids WL: 598.0 MDY: 04.12.2011 DMY: 12.04.2011 MY: 04.2011 GPS: (27.178057, -78.007789)"

SMS_SUBMISSION = "sms"
UNIQUE_VALUE = "unique_value"

#Registration Page Data for Successful Registration Page
REGISTRATION_DATA_FOR_SUCCESSFUL_REGISTRATION = {ORGANIZATION_NAME: "Automation NGO",
                       ORGANIZATION_SECTOR: "PublicHealth",
                       ORGANIZATION_ADDRESS_LINE1: "Panchshil Tech Park, Near Don Bosco School,",
                       ORGANIZATION_ADDRESS_LINE2: "Yerwada",
                       ORGANIZATION_CITY: "Pune",
                       ORGANIZATION_STATE: "Maharashtra",
                       ORGANIZATION_COUNTRY: "India",
                       ORGANIZATION_ZIPCODE: "411006",
                       ORGANIZATION_OFFICE_PHONE: "9876543210",
                       ORGANIZATION_WEBSITE: "http://ngo001.com",
                       TITLE: "Mr.",
                       FIRST_NAME: "Mickey",
                       LAST_NAME: "Jackson",
                       EMAIL: "ngo",
                       REGISTRATION_PASSWORD: "ngo001",
                       REGISTRATION_CONFIRM_PASSWORD: "ngo001",
                       SUCCESS_MESSAGE: "You have successfully registered!! An activation email has been sent to your email address. Please activate before login."}

VALID_ACTIVATION_DETAILS = {ACTIVATION_CODE: "",
                   SUCCESS_MESSAGE: "You have successfully activated your account"}

# valid credentials
VALID_CREDENTIALS = {USERNAME: "",
                     PASSWORD: "ngo001",
                     WELCOME_MESSAGE: "Welcome Mickey!"}

VALID_DATA_FOR_REPORTER = {REPORTER_NAME: "Donald Mouse",
              TELEPHONE_NUMBER: "1234567890",
              COMMUNE: "urbaine",
              GPS: "48.955267  1.816013",
              SUCCESS_MESSAGE: "Registration successful. Reporter identification number: rep1"}

# valid entity data
VALID_SUBJECT_TYPE1 = {ENTITY_TYPE: "Waterpoint", SUCCESS_MESSAGE: "Entity definition successful"}
VALID_SUBJECT_TYPE2 = {ENTITY_TYPE: "Well", SUCCESS_MESSAGE: "Entity definition successful"}

VALID_DATA_FOR_SUBJECT = {ENTITY_TYPE: "Well",
              AUTO_GENERATE: True,
              SHORT_NAME: "",
              NAME: "Well Monodova",
              LOCATION: "Monodova",
              GEO_CODE: "47.411631 28.369885",
              DESCRIPTION: "This is a Well in monodova",
              MOBILE_NUMBER: "3456789012",
              SUCCESS_MESSAGE: "Registration successful. Subject identification number: wel1."}

VALID_DATA_FOR_PROJECT = {PROJECT_NAME: "well morondava", GEN_RANDOM: False,
              PROJECT_BACKGROUND: "This project is created by functional automation suite.",
              PROJECT_TYPE: "survey",
              SUBJECT: "Well",
              DEVICES: "sms,smartphone",
              PAGE_TITLE: "Subjects"}

VALID_DATA_FOR_SUBJECT_QUESTIONNAIRE = {PAGE_TITLE: "Questionnaire"}

QUESTIONNAIRE_DATA = {QUESTIONNAIRE_CODE: "WPS01", GEN_RANDOM: False,
                      DEFAULT_QUESTION: {QUESTION: "What are you reporting on?", CODE: "WID", MIN: "1", MAX: "10"},
                      QUESTIONS: [{QUESTION: "Water Level", CODE: "WL", TYPE: NUMBER, MIN: "1", MAX: "1000"},
                                  {QUESTION: "Date of report in DD.MM.YYY format", CODE: "DMY", TYPE: DATE, DATE_FORMAT: DD_MM_YYYY},
                                  {QUESTION: "Date of report in MM.YYY format", CODE: "MY", TYPE: DATE, DATE_FORMAT: MM_YYYY},
                                  {QUESTION: "Date of report in MM.DD.YYY format", CODE: "MDY", TYPE: DATE, DATE_FORMAT: MM_DD_YYYY},
                                  {QUESTION: "Color of Water", CODE: "WC", TYPE: LIST_OF_CHOICES,
                                   CHOICE: ["LIGHT RED", "LIGHT YELLOW", "DARK YELLOW"],
                                   ALLOWED_CHOICE: ONLY_ONE_ANSWER},
                                  {QUESTION: "Water point admin name", CODE: "WAN", TYPE: WORD, LIMIT: LIMITED, MAX: "10"},
                                  {QUESTION: "Bacterias in water", CODE: "WB", TYPE: LIST_OF_CHOICES,
                                   CHOICE: ["Aquificae", "Bacteroids", "Chlorobia"],
                                   ALLOWED_CHOICE: MULTIPLE_ANSWERS},
                                  {QUESTION: "Geo points of Well", CODE: "GPS", TYPE: GEO}],
                      CHARACTER_REMAINING: "112 / 160 characters used",
                      SUCCESS_MESSAGE: "Your questionnaire has been saved"}

VALID_DATA_FOR_SMS = {SENDER: "1234567890",
              RECEIVER: "",
              SMS: "WPS01 +WID wel1 +wl 598 +DMY 12.04.2011 +MY 04.2011 +MDY 04.12.2011  +wc c +WAN Mr. Tessy +wb ab +GPS 27.178057  -78.007789",
              SUCCESS_MESSAGE: SUCCESS_MESSAGE_TEXT}

SMS_DATA_LOG = {SMS_SUBMISSION: "sms True False wel1 598 12.04.2011 04.2011 04.12.2011 c Mr. Tessy ab 27.178057 -78.007789",
            UNIQUE_VALUE: "Mr. Tessy"}
