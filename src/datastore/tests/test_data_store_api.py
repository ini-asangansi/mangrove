from datetime import datetime
from datastore import entity

from datastore.entity import Entity
from datastore.database import get_db_manager
from datastore.documents import DataRecordDocument
from nose.tools import *

class TestDataStoreApi(object):
    def setup(self):
        e = Entity(entity_type="clinic",location=["India","MH","Pune"])
        self.uuid = e.save()

    def teardown(self):
        e = entity.get(self.uuid)
        get_db_manager().delete(e._entity_doc)

    def test_create_entity(self):
        e = Entity(entity_type="clinic",
                                  location=["India","MH","Pune"]
                                  )
        uuid = e.save()
        assert uuid
        get_db_manager().delete(e._entity_doc)

    def test_get_entity(self):
        e = entity.get(self.uuid)
        assert e.id
        assert e.entity_type == "clinic"

    def test_should_add_location_hierarchy_on_create(self):
        e = Entity(entity_type="clinic",
                                      location=["India","MH","Pune"]
                   )
        uuid = e.save()
        saved = entity.get(uuid)
        hpath = saved._entity_doc.aggregation_paths
        assert_equal (hpath[entity.attribute_names.GEO_PATH],["India","MH","Pune"])

    def test_should_add_entity_type_on_create(self):
        e = Entity(entity_type=["healthfacility","clinic"])
        uuid = e.save()
        saved = entity.get(uuid)
        hpath = saved._entity_doc.aggregation_paths
        assert_equal (hpath[entity.attribute_names.TYPE_PATH],["healthfacility","clinic"])

    def test_should_add_passed_in_hierarchy_path_on_create(self):
        e = Entity(entity_type=["HealthFacility","Clinic"],location=["India","MH","Pune"],aggregation_paths={"org":["TW_Global","TW_India","TW_Pune"],
                                      "levels":["Lead Consultant", "Sr. Consultant", "Consultant"]})
        uuid = e.save()
        saved = entity.get(uuid)
        hpath = saved._entity_doc.aggregation_paths
        assert_equal (hpath["org"],["TW_Global","TW_India","TW_Pune"])
        assert_equal (hpath["levels"],["Lead Consultant", "Sr. Consultant", "Consultant"])



    def test_hierarchy_addition(self):
        e = entity.get(self.uuid)
        org_hierarchy = ["TWGlobal", "TW-India", "TW-Pune"]
        e.add_hierarchy(name="org",value =org_hierarchy)
        e.save()
        saved = entity.get(self.uuid)
        assert saved.hierarchy_tree["org"] == ["TWGlobal", "TW-India", "TW-Pune"]

    def test_hierarchy_addition_should_clone_tree(self):
        e = entity.get(self.uuid)
        org_hierarchy = ["TW", "PS", "IS"]
        e.add_hierarchy(name="org",value = org_hierarchy)
        org_hierarchy[0] = ["NewValue"]
        e.save()
        saved = entity.get(self.uuid)
        assert saved.hierarchy_tree["org"] == ["TW","PS","IS"]

    def test_should_save_hierarchy_tree_only_through_api(self):
        e = entity.get(self.uuid)
        e.hierarchy_tree[entity.attribute_names.GEO_PATH][0]="US"
        e.save()
        saved = entity.get(self.uuid)
        assert saved.hierarchy_tree[entity.attribute_names.GEO_PATH]==["India","MH","Pune"]  # Hierarchy has not changed.

    def test_get_entities(self):
        e2 = Entity("hospital",["India","TN","Chennai"])
        id2 = e2.save()
        entities = entity.get_entities([self.uuid, id2])
        assert_equal (len(entities),2)
        saved = dict([(e.id, e) for e in entities])
        assert_equal (saved[id2].entity_type,"hospital")
        assert_equal (saved[self.uuid].entity_type,"clinic")
        get_db_manager().delete(e2._entity_doc)

    def _create_clinic_and_reporter(self):
        clinic_entity = Entity(entity_type="clinic",
                               location=["India", "MH", "Pune"])
        clinic_entity.save()
        reporter_entity = Entity(entity_type="reporter")
        reporter_entity.save()
        return clinic_entity, reporter_entity

    def test_submit_data_record_to_entity(self):
        clinic_entity, reporter = self._create_clinic_and_reporter()
        data_record = {"medicines": 20 , "beds" :(10,{"notes":"recorded by Mr. xyz","expiry" : datetime(2011,1,12)})}
        data_record_id = clinic_entity.submit_data_record(data_record, reported_on = datetime(2011,1,12),
                                                          reported_by = reporter,
                                                          source = {"phone":1234,"form_id":"hni.1234"})
        assert data_record_id

        # Assert the saved document structure is as expected
        saved = get_db_manager().load(data_record_id, document_class=DataRecordDocument)
        assert_equals(saved.beds,{"value": 10,"metadata":{"notes":"recorded by Mr. xyz","expiry" : '2011-01-12 00:00:00'}} )
        assert_equals(saved.reported_on,datetime(2011,1,12))

        get_db_manager().delete(clinic_entity._entity_doc)
        get_db_manager().delete(saved)
        get_db_manager().delete(reporter._entity_doc)

#    def test_should_switch_database_on_config_change(self):
#        config.set_database("db1")
#        e = Entity("1","test")
#        id = e.save()
#        config.set_database("db2")  #Now change db and try to load entity
#        try:
#            found = entity.get(id)
#        except:
#            found = None
#        assert not found
#        config.set_database("db1")
#        assert entity.get(id)
#
#        Server(config._server).delete("db1")
#        Server(config._server).delete("db2")
#        config.reset()
#        assert_equal(config._db,"mangrove_web")
#        assert_equal(config._server,settings.SERVER)


    def test_should_create_entity_from_document(self):
        existing = entity.get(self.uuid)
        e = Entity(_document = existing._entity_doc)
        assert e._entity_doc is not None
        assert_equal (e.id,existing.id)
        assert_equal (e.entity_type,existing.entity_type)


    #    TODO: Figure out the right way to check for assertion validation
    # Below will fail for any random assetion failure. How do you check specifically for an assertion failure?
    @raises(AssertionError)
    def test_should_fail_create_for_invalid_arguments(self):
        e = Entity(_document = "xyz")




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
#       new_data_record_id=clinic_entity.update_data_record(old_data_record_id, new_data_record,reported_on = datetime(2011,1,13),reported_by = reporter_id, source = {"phone":12345,"form_id":"hni.1234"})
#       assert new_data_record_id
#       assert new_data_record_id != old_data_record_id #Because we want to store all the submissions that come in. The old data is invalidated and the document is not overwritten
#
