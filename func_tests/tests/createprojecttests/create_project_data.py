# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8


##Variables
PROJECT_NAME = "project_name"
PROJECT_BACKGROUND = "project_background"
PROJECT_TYPE = "project_type"
SUBJECT = "subject"
DEVICES = "devices"
ERROR_MSG = "message"
PAGE_TITLE = "page_title"
GEN_RANDOM = "gen_random"


VALID_DATA = {PROJECT_NAME: "Clinic Morondava ", GEN_RANDOM: True,
              PROJECT_BACKGROUND: "This project is created by functional automation suite.",
              PROJECT_TYPE: "survey",
              SUBJECT: "Clinic",
              DEVICES: "sms,smartphone",
              PAGE_TITLE: "Subjects"}

VALID_DATA2 = {PROJECT_NAME: "Water Point2 Morondava ", GEN_RANDOM: True,
              PROJECT_BACKGROUND: "This project is created by functional automation suite.",
              PROJECT_TYPE: "survey",
              SUBJECT: "Waterpoint",
              DEVICES: "sms,smartphone",
              PAGE_TITLE: "Questionnaire"}

BLANK_FIELDS = {PROJECT_NAME: "",
              PROJECT_BACKGROUND: "",
              PROJECT_TYPE: "",
              SUBJECT: "",
              DEVICES: "",
              ERROR_MSG: "Name  This field is required."}
