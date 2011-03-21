from services.repository.connection import Connection
from services.repository.repository import Repository

class EntityManagementService:

    def __init__(self, repository=Repository(Connection())):
        self.repository = repository

    def create_organization(self, organization):
        return self.repository.save(organization)

    def update_organization(self, organization):
        return self.repository.save(organization)