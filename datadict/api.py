#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

"""
API to query the data dictionary.
"""

from couchdb.client import Document
from couchdb.mapping import (TextField, IntegerField, DateField, 
                             DictField, ListField, Mapping)


class Tags(object):
    name = TextField()


class Contraint(object):
    name = TextField()
    value = TextField()


class BasicType(object):

    name = TextField()


class DataType(Document):
    """
        Data Dictionary entry that define a type. 
        
        self.name : name of the type
        self.contraints : List of contraint objects, that are constraints 
                          the data must be following to be valid
        self.tags : datatype is searchable using text tags. Tags are objects
                    too, providing searching capabilities
        self.type : BasicType object giving some primitive type for the data
                    such as int, str, etc
         
    """
    
    name = TextField()
    constraints = DictField(Mapping.build(
        name = TextField(),
        value = TextField()
    ))
    tags = ListField(DictField(TextField()))
    type = TextField()



