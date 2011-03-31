from datastore import entity
from datastore.entity import Entity
from repository.repository import Repository

class TestDataStoreApi(object):
    def setup(self):
        e = Entity(name="Test_Entity",entity_type="clinic",location=["India","MH","Pune"],
                                  attributes={"power_type":"dc"})
        self.uuid = e.save()

    def teardown(self):
        e = entity.get(self.uuid)
        Repository().delete(e.entity_doc)

    def test_create_entity(self):
        e = Entity(name="X",entity_type="clinic",
                                  location=["India","MH","Pune"],
                                  attributes={"power_type":"dc"})
        uuid = e.save()
        assert uuid

    def test_get_entity(self):
        e = entity.get(self.uuid)
        assert e.name == "Test_Entity"

    def test_hierarchy_addition(self):
        e = entity.get(self.uuid)
        org_hierarchy = ["TW", "PS", "IS"]
        e.add_hierarchy(name="org",value =org_hierarchy)
        e.save()
        saved = entity.get(self.uuid)
        assert saved.hierarchy_tree["org"] == ["TW","PS","IS"]

    def test_hierarchy_addition_should_deep_clone_tree(self):
        e = entity.get(self.uuid)
        org_hierarchy = ["TW", "PS", "IS"]
        e.add_hierarchy(name="org",value = org_hierarchy)
        org_hierarchy[0] = ["NewValue"]
        e.save()
        saved = entity.get(self.uuid)
        assert saved.hierarchy_tree["org"] == ["TW","PS","IS"]


    def test_should_save_hierarchy_tree_only_through_api(self):
        e = entity.get(self.uuid)
        e.hierarchy_tree["location"][0]="US"
        e.save()
        saved = entity.get(self.uuid)
        assert saved.hierarchy_tree["location"]==["India","MH","Pune"]  # Hierarchy has not changed.

#    def test_get_entities(self):
#        entity_two = Entity("Clinic2","clinic",["India","TN","Chennai"])
#        id2 = entity_two.save()
#        id_list=[]
#        id_list.append(self.uuid)
#        id_list.append(id2)
#        entity_list = entity.get_entities(id_list)
#        assert len(entity_list) ==2