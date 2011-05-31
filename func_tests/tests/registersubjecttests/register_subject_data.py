# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8


##Variables
ENTITY_TYPE = "entity_type"
SHORT_NAME = "short_name"
AUTO_GENERATE = "auto_generate"
NAME = "name"
LOCATION = "location"
GEO_CODE = "geo_code"
DESCRIPTION = "description"
MOBILE_NUMBER = "mobile_number"
SUCCESS_MSG = "message"
ERROR_MSG = "message"


VALID_DATA = {ENTITY_TYPE: "Clinic",
              SHORT_NAME: "CLI",
              AUTO_GENERATE: "True",
              NAME: "Clinic Monodova",
              LOCATION: "Monodova",
              GEO_CODE: "47.411631 28.369885",
              DESCRIPTION: "This is a clinic in monodova",
              MOBILE_NUMBER: "34567890",
              SUCCESS_MSG: "Thank You for your submission. The short code is - "}

EXISTING_SHORT_CODE = {ENTITY_TYPE: "Clinic",
              SHORT_NAME: "CID001",
              AUTO_GENERATE: "false",
              NAME: "Clinic Amparaky",
              LOCATION: "Amparaky",
              GEO_CODE: "-19.316667 46.633333",
              DESCRIPTION: "This is a clinic in Amparaky",
              MOBILE_NUMBER: "34567890",
              ERROR_MSG: "Entity with short code = CLI001 already exists."}
