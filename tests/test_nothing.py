#!/usr/bin/env python
# encoding: utf-8
"""
test_nothing.py
"""
import sys
import os
from nose.tools import *

def some_function(a_parameter):
    raise Exception("Some exception")

class TestExample:
    def test_abb(self):
        assert_equal('abb', 'abb')
        
    def test_something_raises(self):
        assert_raises(Exception, some_function, 'some parameter')
    
    def test_true(self):
        assert True
    
    def test_setup_is_called_before_tests(self):
        assert self.test_value==3
    
    def setUp(self):
        self.test_value = 3
