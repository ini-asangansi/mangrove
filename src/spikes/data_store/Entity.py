from couchdb.mapping import Field, TextField, DateTimeField, Mapping, ListField, IntegerField, Document, DictField

__author__ = 'apgeorge'

class Entity(Document):
    entity_id = IntegerField()
    type = TextField(default="Entity")
    namespace = TextField()
    created_at = DateTimeField()
    updated_at = DateTimeField()
    location = ListField(TextField())
    name = TextField()
    attr = ListField(DictField(
                Mapping.build(
                    timestamp = DateTimeField(),
                    field = TextField(),
                    value = Field(),
                    type = TextField()
                )
            ))
