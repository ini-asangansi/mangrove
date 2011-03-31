from datastore import entity
from datastore.entity import Entity


class TestDataStoreApi(object):

    def setup(self):
        self.test_entity = Entity(name="Test_Entity",entity_type="clinic",location=["India","MH","Pune"],attributes={"power_type":"dc"})
        self.uuid = self.test_entity.save()
        pass

    def teardown(self):
        pass
        

    def test_create_entity(self):
        e = Entity(name="X",entity_type="clinic",
                                  location=["India","MH","Pune"],
                                  attributes={"power_type":"dc"})
        uuid = e.save()
        assert uuid

    def test_get_entity(self):
        load_entity = entity.get(self.uuid)
        assert load_entity.name == "Test_Entity"

    def test_hierarchy_addition(self):
        load_entity = entity.get(self.uuid)
        org_hierarchy = ["TW", "PS", "IS"]
        load_entity.add_hierarchy(name="org",value =org_hierarchy)
        load_entity.save()
        load_entity2 = entity.get(self.uuid)
        assert load_entity2.hierarchy_tree["org"] == ["TW","PS","IS"]

    def test_hierarchy_addition_should_deep_clone_tree(self):
        load_entity = entity.get(self.uuid)
        org_hierarchy = ["TW", "PS", "IS"]
        load_entity.add_hierarchy(name="org",value = org_hierarchy)
        org_hierarchy[0] = ["NewValue"]
        load_entity.save()
        load_entity2 = entity.get(self.uuid)
        assert load_entity2.hierarchy_tree["org"] == ["TW","PS","IS"]


    def test_should_save_hierarchy_tree_only_through_api(self):
        load_entity = entity.get(self.uuid)
        local_copy = load_entity.hierarchy_tree
        local_copy["location"][0]="US"
        load_entity.save()
        load_entity2 = entity.get(self.uuid)
        assert load_entity2.hierarchy_tree["location"]==["India","MH","Pune"]

#    def test_get_entities(self):
#        entity_two = Entity("Clinic2","clinic",["India","TN","Chennai"])
#        id2 = entity_two.save()
#        id_list=[]
#        id_list.append(self.uuid)
#        id_list.append(id2)
#        entity_list = entity.get_entities(id_list)
#        assert len(entity_list) ==2