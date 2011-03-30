import uuid
import couchdb
from couchdb.mapping import *
import datetime

from datastore import DataStore

class Record(Document):
    document_type = TextField()
    created_at = DateTimeField()
    attributes = DictField()
    entity_id = TextField()

    def __init__(self, id=None, entity_id=None, document_type='record', attributes={}, **kwargs):
        self.data = {}
        super(couchdb.mapping.Document, self).__init__(
            id = id,
            entity_id = entity_id,
            document_type = document_type,
            attributes = attributes,
            created_at = datetime.datetime.now(),
            **kwargs
        )
        self._save()

    def _save(self):
        ds = DataStore()
        ds.store(self)
