from datastore_api.entity import Entity
from datastore_api.entities import query
import unittest

class TestEntity(unittest.TestCase):
    
    def test_create_entity(self):
        entity = Entity(geocode = "1234", geoname = "Ghana", unique_name = "Navio CHPS")
        entity.save()
        self.assertEqual(entity.geoname,'Ghana')
        
    def test_load_entity(self):
        entity = Entity(geocode = "123466", geoname = "Ghana", unique_name = "Navio CHPS")
        entity.save()
        
        loaded_entity = query.get(uuid=entity.uuid)
        self.assertEqual(loaded_entity.uuid, entity.uuid)
        
        
