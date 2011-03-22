from uuid import uuid4
from couchdb.mapping import TextField, ListField, DictField, Field
from services.repository.DocumentBase import DocumentBase

class DataRecord(DocumentBase):
    def __init__(self, id=uuid4().hex, **values):
        DocumentBase.__init__(self, id=id, document_type = 'Entity')
        for key in values:
            if not key in self._fields.keys():
                self.attributes[key] = values[key]

    def __getattr__(self, name):
        if name in self._fields:
            return self.name
        elif name in self.attributes:
            return self.attributes[name]
        else:
            raise AttributeError('%s has no attribute %s' % (self.__class__.__name__, name))

    entity_id = TextField()
    location = ListField(TextField())
    attributes = DictField()
