from couchdb.mapping import DictField, DateTimeField
from databasemanager.document_base import DocumentBase
from databasemanager.raw_field import RawField

class DataRecordDocument(DocumentBase):
    """
        The couch data_record document. It abstracts out the couch related functionality and inherits from the Document class of couchdb-python.
        A schema for the data_record is enforced here.
    """
    def __init__(self, entity=None,reporter=None, source=None,id = None,reported_on = None,attributes=None):
        DocumentBase.__init__(self, id=id, source=source,document_type = 'DataRecord')
        self.attributes = attributes
        self.reported_on = reported_on
        if entity:
            self.entity_backing_field = entity.__dict__.get('_data')
        if reporter:
            self.reporter_backing_field =reporter.__dict__.get('_data')

    def __getattr__(self, name):
        if name == 'entity':
            return self.load_backing_field(self.entity_backing_field)
        elif name == 'reporter':
            return self.load_backing_field(self.reporter_backing_field)
        elif name in self._fields:
            return self.name
        elif name in self.attributes:
            return self.attributes[name]
        else:
            raise AttributeError('%s has no attribute %s' % (self.__class__.__name__, name))

    reported_on = DateTimeField()
    attributes = RawField()
    entity_backing_field = DictField()
    reporter_backing_field = DictField()
    source = DictField()
    def load_backing_field(self,field):
        if field:
            entity = Entity()
            entity.__dict__['_data'] = field
            return entity
        return None

  