Data Store Modeling
===================

* Entity

  {

  UUID: 1234 (An unique ID)

  Created_at: Timestamp

  Updated_at: Timestamp

  Label: patient, reprter... (Set of labels defining the entity and used for UI level design)

  ID's{

  	patient_id: 1223445

	patient_contact_number: 1223445
	
	reporter_id: 32144
	
	reporter_contact_number: 32144
	
      }

  }

* Data_Record
{
	"type": "DataRecord",
	"class": "class.path.ClinicRecord",
	"uuid": "32chr",
	"created_at": "utc timestamp+tz",
	"updated_at": "utc timestamp+tz",
	"entity_uuid": "points to entity 32chr uuid",
	"payload": [
		{
			"timestamp": "ts utc+tz",
			"field": "nr_of_beds",
			"value": 50,
		},
		
		{
			"timestamp": "ts utc+tz",
			"field": "report_month",
			"value": "JAN",
		},
		
		{
			"timestamp": "ts utc+tz",
			"field": "ARV",
			"value": 50,
		},
			
		}
	]
}

