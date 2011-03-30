import unittest

from datastore.entity import *

class TestEntity(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_entity_creation(self):
        attributes = {
            'name': 'test-name',
            'value': 'test-value'
        }
        e = Entity(**attributes)
        self.assertTrue(e.__class__.__name__ == 'Entity')
        for key, value in attributes.iteritems():
            self.assertTrue(hasattr(e, key))
            self.assertTrue(getattr(e, key) == value)
