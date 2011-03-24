from uuid import uuid4
from services.entity_management.entity_management_service import EntityManagementService
from services.entity_management.models import Organization, Entity
from services.repository.connection import Connection
from services.repository.repository import Repository

class TestEntityManagementService:

    test_organization_name = 'test_organization'
    test_entity_id = ''

    def setup(self):
        self.repository = Repository(Connection())

    def teardown(self):
        document = self.repository.load(self.test_entity_id)
        self.repository.delete(document)
        pass

    def test_should_create_organization(self):
        service = EntityManagementService(self.repository)
        organization = Organization(id=uuid4().hex, name = self.test_organization_name)
        organization = service.create_entity(organization)
        self.test_entity_id = organization.id
        loaded_organization = Repository(Connection()).load(organization.id, Organization)
        assert organization.id == loaded_organization.id and organization.name == loaded_organization.name

    def test_should_create_entity(self):
        service = EntityManagementService(self.repository)
        entity = Entity(id=uuid4().hex, name = "TestEntity", entity_type = "TestEntityType",
                        aggregation_trees = {"location": ["India","MH","Pune"], "something": ["A", "B"]},
                        attr1='attr1',attr2='attr2')
        entity= service.create_entity(entity)
        self.test_entity_id = entity.id
        loaded_entity = Repository(Connection()).load(entity.id, Entity)
        assert entity.id == loaded_entity.id and entity.name == loaded_entity.name
        assert len(loaded_entity.aggregation_trees) == 2
        assert loaded_entity.attr1=='attr1'
        assert loaded_entity.attr2=='attr2'

