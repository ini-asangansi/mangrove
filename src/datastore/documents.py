# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from couchdb.mapping import TextField, Document, DateTimeField, DictField, Field
import datetime
from uuid import uuid4
from decimal import Decimal

# This class can take care of non-json serializable objects. Another solution is to plug in a custom json encoder/decoder.
class RawField(Field):
    def _to_python(self, value):
        return value

    def _to_json(self, value):
        self._make_json_serializable(value)
        return value

    def _to_json_serializable(self, val):
        if type(val) in (datetime.datetime, datetime.date, datetime.time, Decimal):  # Convert datetime etc to string for JSON serialization
            return str(val)  # Should this be the ISO Format with 'Z' suffix for datetime? http://couchdbkit.org/docs/api/couchdbkit.schema.properties-pysrc.html#value_to_json
        return val

    def _make_json_serializable(self, collection):
        for key in collection:
            if isinstance(collection[key], dict) or isinstance(collection[key], list):
                self._make_json_serializable(collection[key])
            else:
                collection[key] = self._to_json_serializable(collection[key])

class DocumentBase(Document):
    created_on = DateTimeField()
    last_updated_on = DateTimeField()
    document_type = TextField()

    def __init__(self, id=None, document_type=None, **values):
        if id is None:
            id = uuid4().hex
        Document.__init__(self,id=id, **values)
        self.created_on = datetime.datetime.now()
        self.document_type = document_type

class EntityDocument(DocumentBase):
    """
        The couch entity document. It abstracts out the couch related functionality and inherits from the Document class of couchdb-python.
        A schema for the entity is enforced here.
    """
    
    entity_type = TextField()
    aggregation_paths = DictField()
    
    def __init__(self, id=None,entity_type = None, aggregation_paths = None):
        DocumentBase.__init__(self, id=id, document_type = 'Entity')
        self.aggregation_paths = aggregation_paths or {}
        self.entity_type = entity_type


class DataRecordDocument(DocumentBase):
    """
        The couch data_record document. It abstracts out the couch related functionality and inherits from the Document class of couchdb-python.
        A schema for the data_record is enforced here.
    """
    reported_on = DateTimeField()
    submission_id = TextField()
    attributes = RawField()
    entity_backing_field = DictField()

    def __init__(self, entity=None,id = None, reported_on = None, attributes = None, submission_id = None):
        DocumentBase.__init__(self, id, document_type = 'DataRecord')
        self.attributes = attributes
        self.reported_on = reported_on
        self.submission_id = submission_id

        if entity:
            self.entity_backing_field = entity.__dict__.get('_data')


    def __getattr__(self, name):
        if name == 'entity':
            return self.load_backing_field(self.entity_backing_field)
        elif name in self._fields:
            return self.name
        elif name in self.attributes:
            return self.attributes[name]
        else:
            raise AttributeError('%s has no attribute %s' % (self.__class__.__name__, name))

    def load_backing_field(self,field):
        if field:
            entity = EntityDocument()
            entity.__dict__['_data'] = field
            return entity
        return None


