from couchdb.mapping import TextField, ListField, DateTimeField, DictField, Mapping, Field
from services.repository.DocumentBase import DocumentBase

class Entity(DocumentBase):
    def __init__(self, id=None, **values):
        DocumentBase.__init__(self, id=id, document_type = 'Entity', **values)
    entity_type = TextField()
    name = TextField()
    location = ListField(TextField())

class Organization(Entity):
    def __init__(self, id=None, **values):
        DocumentBase.__init__(self, id=id, entity_type = 'Organization', **values)
    sector = TextField()
    addressline1 = TextField()
    addressline2 = TextField()
    city = TextField()
    state = TextField()
    country = TextField()
    zipcode = TextField()
    office_phone = TextField()
    website = TextField()
    administrators = ListField(TextField)

