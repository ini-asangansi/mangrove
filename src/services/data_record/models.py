from couchdb.mapping import TextField, ListField, DictField, Field, DateTimeField, Mapping
import simplejson
from services.data_record.raw_field import RawField
from services.entity_management.models import Entity
from services.repository.DocumentBase import DocumentBase

class DataRecord(DocumentBase):
    def __init__(self, entity=None,reporter=None, source=None,id = None, **values):
        DocumentBase.__init__(self, id=id, source=source,document_type = 'DataRecord')
        attributes = {}
        for key in values:
            if not key in self._fields.keys():
                attributes[key] = values[key]
        self.attributes = attributes
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



