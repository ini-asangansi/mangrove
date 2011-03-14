from couchdb.mapping import Document, TextField, DateTimeField, ListField, DictField, Mapping, Field, IntegerField, FloatField

class DataRecord2(Document):
    type = TextField(default="Data_Record2")
    namespace = TextField()
    created_at = DateTimeField()
    updated_at = DateTimeField()
    entity_uuid = TextField()
    field_name = TextField()
    value = Field()
    event_time = DateTimeField()
    field_type = TextField(default="Text")

class IntDataRecord2(DataRecord2):
    value = IntegerField()
    field_type = TextField(default="Number")

class FloatDataRecord2(DataRecord2):
    value = FloatField()
    field_type = TextField(default="Number")

class DateTimeDataRecord2(DataRecord2):
    value = DateTimeField()
    field_type = TextField(default="DateTime")

#// Data record schema
#{
#	"type": "DataRecord",
#	"class": "class.path.ClinicRecord",
#	"uuid": "32chr",
#	"created_at": "utc timestamp+tz",
#	"updated_at": "utc timestamp+tz",
#	"entity_uuid": "points to entity 32chr uuid",
#	"payload": [
#		{
#			"timestamp": "ts utc+tz",
#			"field": "nr_of_beds",
#			"value": 50,
#		},
#
#		{
#			"timestamp": "ts utc+tz",
#			"field": "report_month",
#			"value": "JAN",
#		},
#
#		{
#			"timestamp": "ts utc+tz",
#			"field": "ARV",
#			"value": 50,
#		},
#
#		}
#	]
#}            