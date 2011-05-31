# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8


ENTITY_TYPE = 'entity_type'
ERROR_MESSAGE = 'message'
SUCCESS_MESSAGE = 'message'

# valid entity data
VALID_ENTITY = {ENTITY_TYPE: "Hospital", SUCCESS_MESSAGE: "Entity definition successful"}
# already exist entity
ALREADY_EXIST_ENTITY = {ENTITY_TYPE: "clinic", ERROR_MESSAGE: "Type: clinic is already defined"}
# Blank entity
BLANK = {ENTITY_TYPE: "", ERROR_MESSAGE: "This field is required."}
