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

  UUID: Unique ID

  Entity_id: (Entity_ref_id)

  created_at: Timestamp

  key : value

  ``` : `````

  ``` : `````

  ``` : `````

  }
