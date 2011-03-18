from couchdb.mapping import Document, TextField, DateTimeField
from services.repository.DocumentBase import DocumentBase
import random
from django.contrib.auth.models import get_hexdigest

class RegistrationModel(DocumentBase):
    def __init__(self, id=None, **values):
        DocumentBase.__init__(self, id=id, type = 'RegistrationModel', **values)
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
    

