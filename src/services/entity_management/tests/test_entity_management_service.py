from uuid import uuid4
from services.entity_management.entity_management_service import EntityManagementService
from services.entity_management.models import Organization
from services.repository.connection import Connection
from services.repository.repository import Repository

class TestEntityManagementService:

    test_organization_name = 'test_organization'
    test_organization_id = ''
    
    def setup(self):
        self.repository = Repository(Connection())

    def teardown(self):
        document = self.repository.load(self.test_organization_id)
        self.repository.delete(document)

    def test_should_create_organization(self):
        service = EntityManagementService(self.repository)
        organization = Organization(id=uuid4().hex, name = self.test_organization_name)
        organization = service.create_organization(organization)
        self.test_organization_id = organization.id
        loaded_organization = Repository(Connection()).load(organization.id, Organization)
        assert organization.id == loaded_organization.id and organization.name == loaded_organization.name


        
