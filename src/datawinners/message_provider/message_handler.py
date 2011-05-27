# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from mangrove.utils.types import is_empty
from datawinners.message_provider.messages import messages, DEFAULT

def get_exception_message_for(exception, channel=None):
    ex_type = type(exception)
    if channel is not None:
        message_dict = messages.get(ex_type)
        if message_dict is None:
            return exception.message
        message = message_dict.get(channel)
        if is_empty(message):
            message = messages[ex_type].get(DEFAULT)
    else:
        message = messages[ex_type][DEFAULT]
    if exception.data is not None and "%s" in message:
        return message % exception.data
    return message

