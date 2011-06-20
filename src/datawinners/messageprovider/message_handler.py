# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from mangrove.form_model.form_model import NAME_FIELD
from mangrove.utils.types import is_empty
from datawinners.messageprovider.messages import exception_messages, DEFAULT, VALIDATION_FAILURE_ERROR_MESSAGE, \
    success_messages, SUBMISSION, REGISTRATION


def get_exception_message_for(exception, channel=None):
    ex_type = type(exception)
    if channel is not None:
        message_dict = exception_messages.get(ex_type)
        if message_dict is None:
            return exception.message
        message = message_dict.get(channel)
        if is_empty(message):
            message = exception_messages[ex_type].get(DEFAULT)
    else:
        message = exception_messages[ex_type][DEFAULT]
    if exception.data is not None and "%s" in message:
        return message % exception.data
    return message


def get_submission_error_message_for(errors):
    return VALIDATION_FAILURE_ERROR_MESSAGE % ", ".join(errors.keys())


def get_success_msg_for_submission_using(response):
    reporters = response.reporters
    thanks = success_messages[SUBMISSION] % reporters[0].get(NAME_FIELD) if not is_empty(reporters) else success_messages[SUBMISSION] % ""
    stringified_dict = {k:_stringify(v) for k,v in response.processed_data.items()}
    expanded_response = " ".join([": ".join(each) for each in stringified_dict.items()])
    return thanks + expanded_response


def get_success_msg_for_registration_using(response, entity_type):
    resp_string = "%s identification number: %s" % (entity_type, response.short_code)
    return success_messages[REGISTRATION] % resp_string


def _stringify(item):
    if type(item)==list:
        return (',').join(item)
    return str(item)