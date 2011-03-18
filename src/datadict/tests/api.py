#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest
import os
import sys
import datetime

try:
    import json
except ImportError:
    import simplejson as json

test_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(test_dir)
upper_dir = os.path.dirname(project_dir)

sys.path.insert(0, upper_dir)

from datadict.api import DataType
from datadict.connection import Connection
from datadict.basic_types import TypeBase, IntegerType, StringType
from datadict.exceptions import IntegrityError



class TestApi(unittest.TestCase):


    def setUp(self):
    
        Connection(db_name="datadict_test")
        
        self.int = DataType.create(name="int", contraints={'gt': 0}, 
                                   tags=['int', 'test'], 
                                   type="int", description="Integer type")

        self.float = DataType.create(name="float", contraints={'gt': 0}, 
                                     tags=['float', 'test'], 
                                     type="float", description="Float type")       

        self.string = DataType.create(name="string", contraints={'in': 0}, 
                                      tags=['string', 'test'], 
                                      type="str", description="String type")    

        self.date = DataType.create(name="date", contraints={'gt': '2010-12-10'}, 
                                      tags=['date', 'test'], 
                                      type="datetime", description="Date type")  

        self.bool = DataType.create(name="bool", tags=['bool', 'test'], 
                                    type="bool", description="Date type")                                        
        
    def tearDown(self):
        Connection().server.delete("datadict_test")
        Connection().close()


    def test_datatype_attributes(self):
    
        dt = DataType(name="", contraints="", tags="", type="str",
                      version=datetime.datetime.now(), description="")
        
        self.assertTrue(hasattr(dt, 'name'))
        self.assertTrue(hasattr(dt, 'constraints'))
        self.assertTrue(hasattr(dt, 'tags'))
        self.assertTrue(hasattr(dt, 'type'))
        self.assertTrue(hasattr(dt, 'version'))
        self.assertTrue(hasattr(dt, 'description'))
   

    def test_save_datatype(self):
    
        dt = DataType(name="test", contraints={'gt':4}, tags=['foo', 'bar'], 
                      type="int", version=datetime.datetime.now(), 
                      description="Super dupper type")
           
        old_dt = dict(dt.items())   
            
        dt.save()
        
        dt = DataType.load(dt.id)
        new_dt = dict(dt.items())
        del new_dt['_rev']
        
        self.assertEqual(old_dt, new_dt)
    
    
    def test_search_by_tag(self):

        DataType.create(name="test", contraints={'gt':4}, tags=['foo', 'bar'], 
                      type="int", description="Super a type")
         
        DataType.create(name="a", contraints={'gt':4}, tags=['b', 'c'], 
                      type="int", description="Super b type")
     
        DataType.create(name="1", contraints={'gt':4}, tags=['b', 'bar'], 
                      type="int", description="Super dupper type")     
           

        self.assertEqual(len(DataType.with_tags('foo', 'bar')), 1)
    
  
    def test_type_is_a_type_base_instance(self):
        dt = DataType.load(self.int.id)
        self.assertTrue(isinstance(dt.type, TypeBase))
        dt.type = 'str'
        self.assertTrue(isinstance(dt.type, TypeBase))
  

    def test_basic_types_instances_type_match_the_name(self):
        dt = DataType.load(self.int.id)
        self.assertTrue(isinstance(dt.type, IntegerType))
        dt.type = 'str'
        self.assertTrue(isinstance(dt.type, StringType))  
    
  
    def test_you_cant_assign_a_non_compatible_type(self):
        try:
            self.int.type = "test" 
            self.fail()
        except IntegrityError:
            pass
   
    def type_casting_tester(self, datatype, json_value, python_value):
        
        # from json to python to json
        in_python = datatype.to_python(json_value)
        self.assertEqual(in_python, python_value)
        self.assertEqual(datatype.to_json(in_python), json_value)

        # from python to json to python
        in_json = datatype.to_json(python_value)
        self.assertEqual(in_json, json_value)
        self.assertEqual(datatype.to_python(in_json), python_value)   
        
   
    def test_type_casting(self):
        
        # integer
        self.type_casting_tester(self.int, u'123', 123)        
        self.type_casting_tester(self.int, u'-123', -123) 
        self.type_casting_tester(self.int, u'0', 0)   
        
        self.type_casting_tester(self.float, u'123.0', 123.0)        
        self.type_casting_tester(self.float, u'-123.4', -123.4) 
        self.type_casting_tester(self.float, u'0.0', 0.0)           
  
        self.type_casting_tester(self.string, u'123.0', u'123.0')        
        self.type_casting_tester(self.string, u'é', u'é') 
 
        self.type_casting_tester(self.bool, '1', True)        
        self.type_casting_tester(self.bool, '0', False)  
 
        self.type_casting_tester(self.date,  '2011-03-16 20:24:36.307154',
                             datetime.datetime(2011, 3, 16, 20, 24, 36, 307154))        

    def test_datatypes_let_you_import_type_from_black_box(self):
        
        js = json.dumps({
            "record_1": { 'type': self.date.id,
                           'value': '2011-03-16 20:24:36.307154'},
            "record_2": { 'type':  self.string.id,
                           'value': 'test'},
            "record_3": { 'type': self.bool.id,
                           'value': '0'},                          
            "record_4": { 'type': self.float.id,
                           'value': '-123.89'},   
        })

        check = {
            "record_1": datetime.datetime(2011, 3, 16, 20, 24, 36, 307154),
            "record_2": u'test',
            "record_3": 0,                          
            "record_4" :-123.89   
        }

        result = {}
        for name, record in json.loads(js).iteritems():
            type_, value = record.values()
            result[name] = DataType.load(type_).to_python(value)
            
            "record_4": { 'type': "feature",
                           'value': "GR_fJKLMJLM"},  
           DataType.load(type_).to_python(value) 
           
        
        DataType(type_).generate_aggregation_cache(value)
          
        'fdsqfdsf'
        self.assertEqual(check, result)
    
    # next step : casting to georegistry, (not too hard)
                # casting to any entity (hard)
                # validation on basic type (easy now we got auto type loading)
                # custom validation (not hard but long)
                # generating aggration tree for each type ?
                # generate xform typin / validation ?
        
    # priority: casting to georegistry
              # test versioning and load by version
              
    # in clear: data dict is almost good enought for what we want to do
    # we should work on the data store
    # it's dependant for the map reduce 
    # let's freeze the aggregation on that merge the data store with the data dict
    
    
            
"""    
    def test_create_datatype(self):
        dt: DataType("test", {'gt', }, "", "")
     
        
    def test_datatype_should_be_getable_by_name(self):
        self.assertEqual(DataType.get(name='name'),
                         DataType.match(name='name')[0],
                         DatatTypes.search(name='name')[0])
        
 
    def test_datatype_should_be_getable_by_id(self):
        self.assertEqual(DataType.get(name='name'),
                         DataType.match(uuid='uuid')[0],
                         DatatTypes.search(name='uuid')[0]) 
       

    def test_datatype_should_be_searchable_by_tags(self):
        DataType.search(tag=['foo', 'bar'])
        DataType.match(tag=['foo', 'bar'])    
    
    
    def test_datatype_should_be_accessible_with_version(self):
        self.assertEqual(DataType.match(uuid='uuid', version='1'),
                         DatatTypes.search(name='uuid', version='1')[0])          
     
 
    def test_basic_type_should_be_able_to_cast(self):
        python_object = basic_type_instance.cast(value)   
        
        
    def test_constraints_should_be_abel_to_validate(self):
        constraint_object.validate(good_value)
        try:
            constraint_object.validate(good_value)
        except ValidationError as e:
            e.errors

    def test_modify_tags(self):
        #datatype.add_tag(,,,)
        #datatype.remove_tag(,,,)
        pass


    def test_modify_constraints(self):
        #datatype.add_constraints(,,,)
        #datatype.remove_constraints(,,,)
        pass
        

    def test_updating_field_and_saving_save_data_to_db(self):
        #datatype.add_tag(,,,)
        pass


    def test_updating_field_and_saving_save_data_to_db_only_if_it_changed(self):
        pass


    def test_updating_field_and_saving_trigger_intergrity_check(self):
        pass

            
    def test_incompatible_constraints_saving_should_raise_an_error(self):
        pass
    
       """ 
        
if __name__ == '__main__':
    unittest.main()

