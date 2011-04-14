#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Classes representing the basic types of a DataType, holding method
    to cast and validate date matching this type.
"""

import datetime

from couchdb.mapping import BooleanField, DateTimeField

from exceptions import IntegrityError

import settings


class TypeBase(str):
    
    
    def to_json(self, value):
        """ 
            Convert the value to the JSON format. The method to convert it
            depends of the TypeBase child implementation. Default is to 
            call unicode() on the object.
        """
        return unicode(value)
        
        
    def to_python(self, value):
        """ 
            Convert the value to a Python object. The method to convert it
            depends of the TypeBase child implementation. Default is to 
            call unicode() on the object.
        """
        return unicode(value)
        
    
    
class IntegerType(TypeBase):

    def to_python(self, value):
        """ 
            Convert en string representing an integer into a Python int.
        """
        return int(value)
    
    
    
class FloatType(TypeBase):

    def to_python(self, value):
        """ 
            Convert en string representing an float into a Python float.
        """
        return float(value)




class StringType(TypeBase):
    pass
  
    
class DateTimeType(TypeBase):

    
    def to_json(self, value):
        """ 
            Convert en Python boolean into a string representation of a bool.
        """
        return value.strftime(settings.DB_DATE_FORMAT)
        
        
    def to_python(self, value):
        """ 
            Convert en string representing an boolean into a Python bool.
        """
        return datetime.datetime.strptime(value, settings.DB_DATE_FORMAT)
 
    
class BooleanType(TypeBase):


    def to_json(self, value):
        """ 
            Convert en Python boolean into a string representation of a bool.
        """
        return str(int(value))
        
        
    def to_python(self, value):
        """ 
            Convert en string representing an boolean into a Python bool.
        """
        return bool(int(value))
   
    
class FeatureType(TypeBase):
    pass      

class EntityType(TypeBase):
    pass 


class BasicType(object):
    """
       Inherit from the Python String, so is very easy to cast to JSON.
    """

    TYPES = ('int', 'float','str', 'datetime', 'bool', 'feature', 'entity')
    
    TYPES_CLASSES = (IntegerType, FloatType, StringType, DateTimeType,
                     BooleanType, FeatureType, EntityType)
                     
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
