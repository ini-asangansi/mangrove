import uuid
import couchdb
from couchdb.mapping import *
import datetime

from record import Record
from datastore import DataStore

# Module (almost Class) methods

#def get_by_id(self, id):
#    return self.load(ds.db, id)

# Main Entity class

class Entity(couchdb.mapping.Document):
    document_type = TextField()
    entity_type = TextField()
    name = TextField()
    created_at = DateTimeField()
    aggregation_trees = DictField()

    def __init__(self, id=None, document_type='entity', aggregation_trees={}, **kwargs):
        self.data = {}
        if not id: id = uuid.uuid4().hex
        super(couchdb.mapping.Document, self).__init__(
            id = id,
            document_type = document_type,
            aggregation_trees = aggregation_trees,
            created_at = datetime.datetime.now(),
            **kwargs
        )
        self._save()

    def _save(self):
        ds = DataStore()
        ds.store(self)

    def update(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)
        self._save()

    def delete(self):
        pass

    def add_data(self, record):
        pass

    def update_data(self, record):
        pass

    def invalidate_data(self, record):
        pass

    def get_data(self):
        pass
