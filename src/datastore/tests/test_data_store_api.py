from datastore.entity import Entity

__author__ = 'shweta'




class TestDataStoreApi(object):

    def test_create_entity(self):
        entity = Entity({"name":"Test_Entity","entity_type":"clinic","location":["India","MH","Pune"]})
        uuid = entity.save()
        assert uuid

