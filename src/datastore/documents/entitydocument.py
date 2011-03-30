from couchdb.mapping import TextField, ListField, DateTimeField, DictField, Mapping, Field
from services.data_record.raw_field import RawField
from services.repository.DocumentBase import DocumentBase

class EntityDocument(DocumentBase):
    def __init__(self, id=None,name = None, entity_type = None, aggregation_trees={}, **values):
        DocumentBase.__init__(self, id=id, document_type = 'Entity', **values)
        self.aggregation_trees = aggregation_trees
        self.name=name
        self.entity_type = entity_type
        if values:
            self.attributes = values

    entity_type = TextField()
    name = TextField()
    aggregation_trees = DictField()
    attributes = RawField()

    def __getattr__(self,name):
        if name in self._fields:
            return self.name
        elif name in self.attributes:
            return self.attributes[name]
        else:
            raise AttributeError('%s has no attribute %s' % (self.__class__.__name__, name))

