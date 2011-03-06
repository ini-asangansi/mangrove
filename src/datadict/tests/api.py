#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest
import os
import sys
import datetime

test_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(test_dir)
upper_dir = os.path.dirname(project_dir)

sys.path.insert(0, upper_dir)

from datadict.api import DataType
from datadict.connection import Connection

class TestApi(unittest.TestCase):


    def setUp(self):
        Connection(db_name="datadict_test")
        
        
    def tearDown(self):
        Connection().server.delete("datadict_test")
        Connection().close()


    def test_datatype_attributes(self):
    
        dt = DataType(name="", contraints="", tags="", type="",
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
    
      
"""    
    def test_create_datatype(self):
        dt = DataType("test", {'gt', }, "", "")
     
        
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

