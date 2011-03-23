from datetime import datetime
from uuid import uuid4
from couchdb.mapping import TextField, ListField, DictField, Field, DateTimeField, Mapping
from services.entity_management.models import Entity
from services.repository.DocumentBase import DocumentBase

class DataRecord(DocumentBase):
    def __init__(self, entity=None, id = None, **values):
        DocumentBase.__init__(self, id=id, document_type = 'DataRecord')
        for key in values:
            if not key in self._fields.keys():
                self.attributes[key] = str(values[key])
        if entity:
            self.entity_backing_field = entity.__dict__

    def __getattr__(self, name):
        if name == 'entity':
            return self.load_entity()
        elif name in self._fields:
            return self.name
        elif name in self.attributes:
            return self.attributes[name]
        else:
            raise AttributeError('%s has no attribute %s' % (self.__class__.__name__, name))

    attributes = DictField()
    entity_backing_field = DictField()

    def load_entity(self):
        if self.entity_backing_field:
            entity = Entity()
            entity.__dict__.update(self.entity_backing_field)
            return entity
        return None


