#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

"""
API to query the data dictionary.
"""

import datetime
from uuid import uuid4

from couchdb.mapping import (TextField, IntegerField, DateField, 
                             DictField, ListField, Mapping, DateTimeField,
                             Document)

from connection import Connection
from basic_types import BasicType


class DataDictDocument(Document):
    """
        Common struture for all Document object we are retriving from
        CouchDb for the datadict.
    """
    
    def __init__(self, *args, **kwargs):
        Document.__init__(self, *args, **kwargs)
        if not getattr(self, 'id', None):
            self.id = uuid4().hex
    
    @classmethod
    def load(cls, id):
        """
            Override the native one to remove the db as 
            an argument and use the singleton
        """
        doc = Connection().db.get(id)
        if doc is None:
            return None
        return cls.wrap(doc)
    
    
    def save(self):
        """
            Override the native one to remove the db as 
            an argument and use the singleton
        """
        return self.store(Connection().db)
    
    
    @classmethod 
    def create(cls, *args, **kwargs):
        obj = cls(*args, **kwargs)
        obj.save()
        return obj
        
        
    @classmethod
    def query(cls, map_function, reduce_func="", 
              *args, **kwargs):
        return Document.query(Connection().db, map_function, 
                              reduce_func, *args, **kwargs)
        
    

class Tags(DataDictDocument):
    name = TextField()


class Contraint(DataDictDocument):
    name = TextField()
    value = TextField()



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
    
    name = TextField()
    constraints = DictField()
    tags = ListField(TextField())
    type = TextField()
    version = DateTimeField()
    description = TextField()


    def __init__(self, *args, **kwargs):
        DataDictDocument.__init__(self, *args, **kwargs)
        if not hasattr(self, 'version'):
            self.version = datetime.datetime.now()
        
        # set the type manually since we by pass the normal behavior
        self._data['type'] = BasicType.clean(kwargs.get('type', ''))
        
            
    # this ensure that type is casted from a string to a BasicType instance
    @property
    def type(self):
        return BasicType(self._data['type'])

    @type.setter
    def type(self, value):
        self._data['type'] = BasicType.clean(value)


    
    def to_json(self, value):
        """ 
            Convert the value to the JSON format. The method delegate
            this behavior to the current basic type object.
        """
        return self.type.to_json(value)
        
        
    def to_python(self, value):
        """ 
            Convert the value to a Python object. The method delegate
            this behavior to the current basic type object.
        """
        return self.type.to_python(value)
        

    # todo: escape this
    # I can't believe there is no better way to do this. Please somebody
    # tell me that I'm completly wrong and that couchdb does let me pass
    # parameters in some ways other than just the key in GET
    @classmethod
    def with_tags(cls, *tags):
        """
            Return document with that have all these tags
        """
        
        query = """
                function(doc) {

                    var expected_tags = ['%s'],
                        tags = doc.tags,
                        ecount = expected_tags.length;

                    for(var i = 0; i < ecount; i++) {
                        if(tags.indexOf(expected_tags[i]) == -1) {
                            return false;
                        }
                    }

                    emit(tags, doc);

                }
        """ % "', '".join(tags)
        
        return cls.query(query)
       
       
    @classmethod
    def load(cls, id):
        """
            Override the parent method to allow type checking.
        """
        doc = Connection().db.get(id)
        if doc is None:
            return None
        instance = cls(type=doc['type'])
        instance._data.update(doc)
        return instance  
         
