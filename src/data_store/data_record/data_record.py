from couchdb.mapping import Document, TextField, DateTimeField, Field, IntegerField, FloatField

class DataRecord(Document):
    type = TextField(default="Data_Record2")
    namespace = TextField()
    created_at = DateTimeField()
    updated_at = DateTimeField()
    entity_uuid = TextField()
    field_name = TextField()
    value = Field()
    event_time = DateTimeField()
    field_type = TextField(default="Text")

class IntDataRecord(DataRecord):
    value = IntegerField()
    field_type = TextField(default="Number")

class FloatDataRecord(DataRecord):
    value = FloatField()
    field_type = TextField(default="Number")

class DateTimeDataRecord(DataRecord):
    value = DateTimeField()
    field_type = TextField(default="DateTime")
