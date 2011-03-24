from time import sleep
from services.entity_management.organization_id_creator import OrganizationIdCreator

class TestOrganizationIdGenerator:
    def setup(self):
        self.organizationIdCreator=OrganizationIdCreator()


    def test_creation_of_organization_id(self):
        generated_id_1 = self.organizationIdCreator.generateId()
        generated_id_2 = self.organizationIdCreator.generateId()
        assert generated_id_1
        assert generated_id_2
        assert generated_id_1 != generated_id_2
