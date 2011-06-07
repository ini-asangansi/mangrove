# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

##Variables
SMS_SUBMISSION = "sms"
UNIQUE_VALUE = "unique_value"
FAILURE_MSG = "failure_msg"

SMS_DATA_LOG = {SMS_SUBMISSION: "sms True cid005 Mr. Tessy 58 17.05.2011 b ade",
            UNIQUE_VALUE: "Mr. Tessy"}

EXCEED_WORD_LIMIT_LOG = {SMS_SUBMISSION: "sms False CID005 Mr. O'brain 58 17.05.2011 b ade",
            UNIQUE_VALUE: "Mr. O'brain",
            FAILURE_MSG: "Answer Mr. O'brain for question NA is longer than allowed."}

EXTRA_PLUS_IN_BTW_LOG = {SMS_SUBMISSION: "sms True cid002 Mr. Dessy 58 17.05.2011 b ade",
            UNIQUE_VALUE: "Mr. Dessy"}

PLUS_IN_THE_BEGINNING_LOG = {SMS_SUBMISSION: "sms False CID005 Mr. O'brain 58 17.05.2011 b ade",
            UNIQUE_VALUE: "Mr. O'brain",
            FAILURE_MSG: "Answer Mr. O'brain for question NA is longer than allowed."}