from services.entity_management.models import Organization, Entity
from services.repository.connection import Connection
from services.repository.repository import Repository

class EntityManagementService:

    def __init__(self, repository=Repository(Connection())):
        self.repository = repository

    def create_entity(self, entity):
        return self.repository.save(entity)

    def load_entity(self, id, entity = Entity):
        return self.repository.load(id, entity)

    def update_entity(self, entity):
        return self.repository.save(entity, entity.__class__)
