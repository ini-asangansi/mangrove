from couchdb.mapping import TextField, ListField, DateTimeField, DictField, Mapping, Field
from databasemanager.document_base import DocumentBase
from services.data_record.raw_field import RawField


class EntityDocument(DocumentBase):
    """
        The couch entity document. It abstracts out the couch related functionality and inherits from the Document class of couchdb-python.
        A schema for the entity is enforced here.
    """

    def __init__(self, id=None,entity_type = None, aggregation_trees = None):
        DocumentBase.__init__(self, id=id, document_type = 'Entity')
        self.aggregation_trees = aggregation_trees or {}
        self.entity_type = entity_type

    entity_type = TextField()
    aggregation_trees = DictField()

