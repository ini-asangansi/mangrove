# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from numbers import Number

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
    except:
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
    '''True if arg is any type in Pythons "number tower"'''
    return isinstance(arg, Number)

def string_as_bool(arg):
    '''True if the argument is any of ("t", "true", "y", "yes", "1", false otherwise'''
    if arg is not None and unicode(arg).lower() in (u'y', u'yes', u't', u'true', u'1'):
        return True
    return False