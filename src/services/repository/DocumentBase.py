from datetime import datetime
from uuid import uuid4
from couchdb.mapping import Document, DateTimeField, TextField

class DocumentBase(Document):
    def __init__(self, id=None, type=None, **values):
        if id is None:
            id = uuid4().hex
        Document.__init__(self,id=id, **values)
        self.created_on = datetime.utcnow()
        self.type = type

    created_on = DateTimeField()
    last_updated_on = DateTimeField()
    type = TextField()
  