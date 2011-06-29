# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
import unittest
from datawinners.location.LocationTree import LocationTree


class TestLocationTree(unittest.TestCase):
    def setUp(self):
        self.tree = LocationTree()


    def tearDown(self):
        pass

    def test_load_tree(self):
        self.assertEqual('Madagascar', self.tree.countries[0])
        self.assertEqual(6, len(self.tree.get_next_level('Madagascar')))

    def test_get_hierarchy_from_location(self):
        self.assertEqual(self.tree.get_hierarchy_path('Amboahangibe'),
            ['Madagascar', 'Antsiranana', 'Sava', 'Sambava', 'Amboahangibe'])

    def test_is_valid_location(self):
        self.assertTrue(self.tree.exists("Amboahangibe"))
        self.assertFalse(self.tree.exists("XYZ"))

    def test_should_get_lowest_admin_location_for_geocode(self):
        self.assertEqual("Ambatomanjaka",self.tree.get_location_for_geocode(lat=-18.777180,long=46.854321 ))
        self.assertFalse(self.tree.exists("XYZ"))




