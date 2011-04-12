# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from numbers import Number
from datetime import datetime
import iso8601
import pytz
try:
    import json
except ImportError:
    import simplejson as json

def is_empty(arg):
    '''Generalizes 'empty' checks on Strings, sequences, and dicts.
        Returns 'True' for None, empty strings, strings with just white-space,
        and sequences with len == 0
        '''
    if arg is None:
        return True

    if is_string(arg):
        arg = arg.strip()

    try:
        if len(arg) == 0:
            return True
    except TypeError:
        # wasn't a sequence
        pass

    return False

def is_not_empty(arg):
    '''Convenience inverse of is_empty '''
    return not is_empty(arg)

def is_sequence(arg):
    '''Returns True is passed arg is an iterable sequence'''
    return hasattr(arg, '__iter__')

def is_string(arg):
    '''Test for string in proper way to handle both strings and unicode strings'''
    return isinstance(arg, basestring)

def is_number(arg):
    '''True if arg is any type in Pythons "number tower"

    **Note** This includes Booleans!
    '''
    return isinstance(arg, Number)

def string_as_bool(arg):
    '''True if the argument is any of ("t", "true", "y", "yes", "1", false otherwise'''
    if arg is not None and unicode(arg).lower() in (u'y', u'yes', u't', u'true', u'1'):
        return True
    return False

def primitive_type(arg):
    ''' Returns a string representing the primitive type.

    Options are: 'unknown' 'boolean', 'numeric', 'text', 'datetime'
    '''
    # TODO: Should we have a 'coordinate' or geocode type?
    typ = 'unknown'
    if isinstance(arg, bool):
        typ = 'boolean'
    elif is_number(arg):
        typ = 'numeric'
    elif isinstance(arg, datetime):
        typ = 'datetime'
    elif is_string(arg):
        typ = 'text'

    return typ

#
# Date helpers
#


def is_naive_datetime(d):
    assert isinstance(d, datetime)
    return (d.tzinfo is None)

def to_aware_utc(d):
    '''Returns a tz aware datetime in UTC for given datetime.

    NOTE: if passed in datetime is naive, it assumes it is in UTC
    '''
    assert isinstance(d, datetime)
    if is_naive_datetime(d):
        # assume was in UTC!
        d = d.replace(tzinfo = pytz.UTC)
    else:
        d = d.astimezone(pytz.UTC)
    return d

def to_naive_utc(d):
    '''Returns a naive (no timezone) datetime in UTC.

    NOTE: if inbound datetime is naive, it assumes it's already UTC and returns as is
    '''
    assert isinstance(d, datetime)
    if not is_naive_datetime(d):
        d = d.astimezone(pytz.UTC).replace(tzinfo = None)
    return d

def utcnow():
    return to_aware_utc(datetime.utcnow())

def py_datetime_to_js_datestring(d):
    if not isinstance(d, datetime):
        raise ValueError("not a datetime")
    return to_aware_utc(d).isoformat()

def js_datestring_to_py_datetime(s):
    if not is_string(s):
        raise ValueError("Not a valid string")
    if is_empty(s):
        raise ValueError("Not a valid datetime string")

    # wrap call to iso8601 parser to return ValueError on
    # all failures
    try:
        return to_aware_utc(iso8601.parse_date(s))
    except Exception:
        raise ValueError("datestring not valid format")


#
# JSON Helpers
#

class _json_encoder(json.JSONEncoder):
    def default(self, o):
       try:
           return py_datetime_to_js_datestring(o)
       except ValueError:
           # wasn't a date
           pass
       return json.JSONEncoder.default(self, o)

def _decode_hook(s):
    out = {}
    for k in s:
        v = s[k]
        if isinstance(v, basestring):
            try:
                v = js_datestring_to_py_datetime(v)
            except ValueError:
                # wasn't a date
                pass
        elif not isinstance(v, dict) and is_sequence(v):
            # it's a sequence that isn't a dict, so process it
            newv = []
            for i in v:
                try:
                    i = js_datestring_to_py_datetime(i)
                except ValueError:
                    # wasn't a date
                    pass
                newv.append(i)
                v = newv
        out[k] = v
    return out

def decode_json(s):
    return json.loads(s, object_hook = _decode_hook)

def encode_json(o):
    return json.dumps(o, cls = _json_encoder)

