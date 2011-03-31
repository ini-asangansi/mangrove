from datastore.entity import Entity
from datastore.entities import query
import unittest
import datetime

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
        
        
    def test_enity_has_created_at(self):
        entity = Entity(geocode = "1234", geoname = "Accra", unique_name = "Kajelo CHPS")
        entity.save()
        #FIXME Need Py2.7 to run the below code.
        #self.assertIfNotNone(entity.created_at)

    def test_add_data_record_to_entity(self):
        entity = Entity(geocode = "1234", geoname = "Accra", unique_name = "Kajelo CHPS")
        entity.save()

        data_record = entity.submit_datarecord(record_dict = {'arv': '40'}, created_at = datetime.datetime.now())
        data_record.save()
        self.assertEqual(data_record.for_entity_uuid, entity.uuid)

    def test_if_reported_at_attribute_is_created(self):
        entity = Entity(geocode = "1234", geoname = "Accra", unique_name = "Kajelo CHPS")
        entity.save()

        data_record = entity.submit_datarecord(record_dict = {'arv': '40'}, created_at = datetime.datetime.now())
        data_record.save()
        self.assertEqual(data_record.reported_at.date(), datetime.datetime.now().date())
