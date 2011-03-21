from couchdb.mapping import TextField, ListField
from services.repository.DocumentBase import DocumentBase

class OrganizationModel(DocumentBase):
    def __init__(self, id=None, **values):
        DocumentBase.__init__(self, id=id, type = 'OrganizationModel', **values)
    name = TextField()
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




