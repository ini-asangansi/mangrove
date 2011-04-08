# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from couchdb.mapping import TextField, Document, DateTimeField, DictField, Field
import datetime
from uuid import uuid4
from decimal import Decimal


class attributes(object):
    '''Constants for referencing standard attributes in docs.'''
    MODIFIED = 'modified'
    CREATED = 'created'
    EVENT_TIME = 'event_time'
    ENTITY_ID = 'entity_id'
    SUBMISSION_ID = 'submission_id'
    AGG_PATHS = 'aggregation_paths'
    GEO_PATH = '_geo'
    TYPE_PATH = '_type'
    DATA = 'data'

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
    created = DateTimeField()
    modified = DateTimeField()
    document_type = TextField()

    def __init__(self, id = None, document_type=None, **values):
        if id is None:
            id = uuid4().hex
        Document.__init__(self,id=id, **values)
        self.created = datetime.datetime.utcnow()
        self.document_type = document_type

class EntityDocument(DocumentBase):
    """
        The couch entity document. It abstracts out the couch related functionality and inherits from the Document class of couchdb-python.
        A schema for the entity is enforced here.
    """
    aggregation_paths = DictField()
    
    def __init__(self, id=None, aggregation_paths = None):
        DocumentBase.__init__(self, id = id, document_type = 'Entity')
        self.aggregation_paths = (aggregation_paths if aggregation_paths is not None else {})

    @property
    def entity_type(self):
        if attributes.TYPE_PATH in self.aggregation_paths:
            return self.aggregation_paths[attributes.TYPE_PATH]
        else:
            return None

    @entity_type.setter
    def entity_type(self, typ):
        self.aggregation_paths[attributes.TYPE_PATH] = typ

    @property
    def location(self):
        if attributes.GEO_PATH in self.aggregation_paths:
            return self.aggregation_paths[attributes.GEO_PATH]
        else:
            return None

    @location.setter
    def location(self, loc):
        self.aggregation_paths[attributes.GEO_PATH] = loc


class DataRecordDocument(DocumentBase):
    """
        The couch data_record document. It abstracts out the couch related functionality and inherits from the Document class of couchdb-python.
        A schema for the data_record is enforced here.
    """
    data = RawField()
    entity_backing_field = DictField()
    submission_id = TextField()
    event_time =  DateTimeField()

    def __init__(self, id = None, entity_doc = None, event_time = None, submission_id = None, data = None):
        assert entity_doc is None or isinstance(entity_doc, EntityDocument)
        DocumentBase.__init__(self, id, 'DataRecord')
        self.submission_id = submission_id
        self.data = data
        self.event_time = event_time
        
        if entity_doc:
            self.entity_backing_field = entity_doc.unwrap()

