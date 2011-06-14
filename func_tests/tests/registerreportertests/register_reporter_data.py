# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8


##Variables
NAME = "name"
TELEPHONE_NUMBER = "telephone_number"
COMMUNE = "commune"
GPS = "gps"
SUCCESS_MSG = "message"
ERROR_MSG = "message"


BLANK_FIELDS = {NAME: "",
                TELEPHONE_NUMBER: "",
                COMMUNE: "",
                GPS: "",
                ERROR_MSG: "Required information for registration. Please fill out at least one location field correctly.* Name   This field is required.* Mobile Number   This field is required."}

VALID_DATA = {NAME: "Mickey Duck",
              TELEPHONE_NUMBER: "9876543210",
              COMMUNE: "urbaine",
              GPS: "48.955267  1.816013",
              SUCCESS_MSG: "Registration successful. Reporter identification number: rep"}
