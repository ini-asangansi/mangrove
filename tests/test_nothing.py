#!/usr/bin/env python
# encoding: utf-8
"""
test_nothing.py
"""

import sys
import os

class TestExample:
    def setUp(self):
        self.test_value = 3
    
	def test_abb(self):
		assert 'abb'=='abb'
	def test_true(self):
		assert True
	
	def test_setup_is_called_before_tests(self):
	    assert self.test_value==3
