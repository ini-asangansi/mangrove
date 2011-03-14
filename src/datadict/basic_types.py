#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Classes representing the basic types of a DataType, holding method
    to cast and validate date matching this type.
"""

from exceptions import IntegrityError


class TypeBase(str):
    pass
    
class IntegerType(TypeBase):
    pass
    
class FloatType(TypeBase):
    pass

class StringType(TypeBase):
    pass
    
class DateTimeType(TypeBase):
    pass
    
class BooleanType(TypeBase):
    pass  
    
class FeatureType(TypeBase):
    pass      


class BasicType(object):
    """
       Inherit from the Python String, so is very easy to cast to JSON.
    """

    TYPES = ('int', 'float','str', 'datetime', 'bool', 'feature')
    
    TYPES_CLASSES = (IntegerType, FloatType, StringType, DateTimeType,
                     BooleanType, FeatureType)
                     
    TYPES_NAMES_TO_CLASSES = zip(TYPES, TYPES_CLASSES)

    
    def __new__(cls, *args, **kwargs):
        """
            Create the proper BasicType according to the name passed
        """
        
        try:
            type_name = cls.clean(args[0])
        except IndexError:
            raise IntegrityError('You must pass a type name as a first non '\
                                 'non keyword argument')
    
        mapping = dict(cls.TYPES_NAMES_TO_CLASSES)
        klass = mapping[type_name]

        return type(klass.__name__, (klass, ), {})(type_name)

       
    @classmethod
    def clean(cls, type_name):
        """
            Normalize the type name, then check if it is a valid type name.
        """
        type_name = type_name.lower()
        if type_name not in cls.TYPES:
            raise IntegrityError('"%(type_name)s" is not a valid type name. '\
                                 'Choose among: "%(allowed_type_names)s"' % {
                                 'type_name': type_name,
                                 'allowed_type_names': '", "'.join(cls.TYPES) })
        return type_name
