from datetime import datetime
from datastore import entity
from datastore.entity import Entity
from datastore.database import get_db_manager, _delete_db_and_remove_db_manager
from datastore.documents import DataRecordDocument, attributes
import unittest

class TestDataStoreApi(unittest.TestCase):
    def setUp(self):
        self.dbm = get_db_manager(database='mangrove-test')
        e = Entity(self.dbm, entity_type="clinic", location=["India","MH","Pune"])
        self.uuid = e.save()

    def tearDown(self):
        del self.dbm.database[self.uuid]
        _delete_db_and_remove_db_manager(self.dbm)

    def test_create_entity(self):
        e = Entity(self.dbm, entity_type="clinic", location=["India","MH","Pune"])
        uuid = e.save()
        self.assertTrue(uuid)
        self.dbm.delete(e._doc)

    def test_get_entity(self):
        e = entity.get(self.dbm, self.uuid)
        self.assertTrue(e.id)
        self.assertTrue(e.type_string == "clinic")

    def test_should_add_location_hierarchy_on_create(self):
        e = Entity(self.dbm, entity_type="clinic", location=["India","MH","Pune"])
        uuid = e.save()
        saved = entity.get(self.dbm, uuid)
        self.assertEqual(saved.location_path,["India","MH","Pune"])

    def test_should_add_entity_type_on_create(self):
        e = Entity(self.dbm, entity_type=["healthfacility","clinic"])
        uuid = e.save()
        saved = entity.get(self.dbm, uuid)
        self.assertEqual(saved.type_path,["healthfacility","clinic"])

    def test_should_add_entity_type_on_create_as_aggregation_tree(self):
        e = Entity(self.dbm, entity_type="health_facility.clinic")
        uuid = e.save()
        saved = entity.get(self.dbm, uuid)
        self.assertEqual(saved.type_path,["health_facility","clinic"])

    def test_should_add_passed_in_hierarchy_path_on_create(self):
        e = Entity(self.dbm, entity_type=["HealthFacility","Clinic"],location=["India","MH","Pune"],aggregation_paths={"org": ["TW_Global","TW_India","TW_Pune"],
                                      "levels": ["Lead Consultant", "Sr. Consultant", "Consultant"]})
        uuid = e.save()
        saved = entity.get(self.dbm, uuid)
        hpath = saved._doc.aggregation_paths
        self.assertEqual(hpath["org"],["TW_Global","TW_India","TW_Pune"])
        self.assertEqual(hpath["levels"],["Lead Consultant", "Sr. Consultant", "Consultant"])

    def test_hierarchy_addition(self):
        e = entity.get(self.dbm, self.uuid)
        org_hierarchy = ["TWGlobal", "TW-India", "TW-Pune"]
        e.set_aggregation_path("org", org_hierarchy)
        e.save()
        saved = entity.get(self.dbm, self.uuid)
        self.assertTrue(saved.aggregation_paths["org"] == ["TWGlobal", "TW-India", "TW-Pune"])

    def test_hierarchy_addition_should_clone_tree(self):
        e = entity.get(self.dbm, self.uuid)
        org_hierarchy = ["TW", "PS", "IS"]
        e.set_aggregation_path("org", org_hierarchy)
        org_hierarchy[0] = ["NewValue"]
        e.save()
        saved = entity.get(self.dbm, self.uuid)
        self.assertTrue(saved.aggregation_paths["org"] == ["TW","PS","IS"])

    def test_should_save_hierarchy_tree_only_through_api(self):
        e = entity.get(self.dbm, self.uuid)
        e.location_path[0]="US"
        e.save()
        saved = entity.get(self.dbm, self.uuid)
        self.assertTrue(saved.location_path==["India","MH","Pune"])  # Hierarchy has not changed.

    def test_get_entities(self):
        e2 = Entity(self.dbm, "hospital",["India","TN","Chennai"])
        id2 = e2.save()
        entities = entity.get_entities(self.dbm, [self.uuid, id2])
        self.assertEqual(len(entities),2)
        saved = dict([(e.id, e) for e in entities])
        self.assertEqual(saved[id2].type_string, "hospital")
        self.assertEqual(saved[self.uuid].type_string,"clinic")
        self.dbm.delete(e2._doc)

    def _create_clinic_and_reporter(self):
        clinic_entity = Entity(self.dbm, entity_type="clinic",
                               location=["India", "MH", "Pune"])
        clinic_entity.save()
        reporter_entity = Entity(self.dbm, entity_type="reporter")
        reporter_entity.save()
        return clinic_entity, reporter_entity

    def test_add_data_record_to_entity(self):
        clinic_entity, reporter = self._create_clinic_and_reporter()
        data_record = [("medicines", 20), ("doctor", "aroj"), ('facility', 'clinic', 'facility_type')]
        data_record_id = clinic_entity.add_data(data = data_record,
                                                event_time = datetime(2011,01,02), submission_id = "123456")
        self.assertTrue(data_record_id is not None)

        # Assert the saved document structure is as expected
        saved = self.dbm.load(data_record_id, document_class=DataRecordDocument)
        self.assertEquals(saved.data['medicines']['value'], 20)
        self.assertEquals(saved.event_time,datetime(2011,01,02))
        self.assertEquals(saved.submission_id,"123456")

        self.dbm.delete(clinic_entity._doc)
        self.dbm.delete(saved)
        self.dbm.delete(reporter._doc)

#    def test_should_switch_database_on_config_change(self):
#        config.set_database("db1")
#        e = Entity(self.dbm, "1","test")
#        id = e.save()
#        config.set_database("db2")  #Now change db and try to load entity
#        try:
#            found = entity.get(self.dbm, id)
#        except:
#            found = None
#        assert not found
#        config.set_database("db1")
#        assert entity.get(self.dbm, id)
#
#        Server(config._server).delete("db1")
#        Server(config._server).delete("db2")
#        config.reset()
#        assert_equal(config._db,"mangrove_web")
#        assert_equal(config._server,settings.SERVER)

    def test_should_create_entity_from_document(self):
        existing = entity.get(self.dbm, self.uuid)
        e = Entity(self.dbm, _document = existing._doc)
        self.assertTrue(e._doc is not None)
        self.assertEqual(e.id,existing.id)
        self.assertEqual(e.type_path,existing.type_path)

    def test_should_fail_create_for_invalid_arguments(self):
        with self.assertRaises(AssertionError):
            e = Entity(self.dbm, _document = "xyz")




#    def test_get_current_state(self):
#        clinic_entity, reporter_id = self.create_clinic_and_reporter()
#        data_record = {"numbeds" :{"value": 10,"notes":"recorded by Mr. xyz"}, "nummedicines" : {"value":20}}
#        data_record_id = clinic_entity.submit_data_record(data_record, reported_on = datetime(2011,1,12),reported_by = reporter_id, source = {"phone":1234,"form_id":"hni.1234"})
#        current_state_dict = clinic_entity.current_state()
#        assert current_state_dict["numbeds"]== {"value": 10,"notes":"recorded by Mr. xyz"}
#        assert current_state_dict["nummedicines"]== {"value": 20}
#
#    def test_update_data_record_of_entity(self):
#       clinic_entity, reporter_id = self.create_clinic_and_reporter()
#       data_record = {"numbeds" :{"value": 10,"notes":"recorded by Mr. xyz"}, "nummedicines" : {"value":20}}
#       old_data_record_id = clinic_entity.submit_data_record(data_record, reported_on = datetime(2011,1,12),reported_by = reporter_id, source = {"phone":1234,"form_id":"hni.1234"})
#       new_data_record = {"numbeds" :{"value": 30,"notes":"recorded by Mr. xyz"}, "numdoctors" : {"value":5}}
#       new_data_record_id=clinic_entity.update_data_record(old_data_record_id, new_data_recordtan = datetime(2011,1,13),reported_by = reporter_id, source = {"phone":12345,"form_id":"hni.1234"})
#       assert new_data_record_id
#       assert new_data_record_id != old_data_record_id #Because we want to store all the submissions that come in. The old data is invalidated and the document is not overwritten
#
