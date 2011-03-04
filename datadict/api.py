#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

"""
API to query the data dictionary.
"""

import datetime
from uuid import uuid4

from couchdb.client import Document
from couchdb.mapping import (TextField, IntegerField, DateField, 
                             DictField, ListField, Mapping, DateTimeField)

from connection import Connection

class DataDictDocument(Document):
    """
        Common struture for all Document object we are retriving from
        CouchDb for the datadict.
    """
    
    
    def __init__(self, *args, **kwargs):
        Document.__init__(self, *args, **kwargs)
        if '_id' not in self:
            self['_id'] = uuid4().hex
            self['_rev'] = 0
    
    def save(self):
        self.store(Connection().db)
    

class Tags(DataDictDocument):
    name = TextField()


class Contraint(DataDictDocument):
    name = TextField()
    value = TextField()


class BasicType(DataDictDocument):

    name = TextField()


class DataType(DataDictDocument):
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
    
    """
    def validate(value)
    
    def to_python()
    
    def to_fdjsqkfjqsdlkf()
    """
    

    name = TextField()
    constraints = DictField(Mapping.build(
        name = TextField(),
        value = TextField()
    ))
    tags = ListField(DictField(TextField()))
    type = TextField()
    version = DateTimeField(default=datetime.datetime.now)



