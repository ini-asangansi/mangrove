The DataStore API
=================

In couch- the db will look something like this:

Entity Document::

 {
   "_id": "6",
   "_rev": "1-b6abf6d5d9f81c3ab2584c80c908e2ef",
   "name": "Clinic 6",
   "entity_type": "clinic",
   "last_updated_on": null,
   "created_on": "2011-03-23T13:17:02Z",
   "location": [
       "India",
       "Maharashtra",
       "Pune"
   ],
   "document_type": "Entity"
 }

Data Record for the above Clinic entity::

 {
   "_id": "d7b4f6c0be27491db152550d9717b2bb",
   "_rev": "1-bdbdb7534e0bfa82e0ce3ce5a47624ca",
   "last_updated_on": null,
   "created_on": "2011-03-23T13:17:02Z",
   "attributes": {
       "beds": "50",
       "arv": "150",
       "event_time": "2011-02-01 00:00:00"
   },
   "document_type": "DataRecord",
   "entity_backing_field": {
       "_data": {
           "_id": "3",
           "name": "Clinic 3",
           "entity_type": "clinic",
           "_rev": "1-4cec92743969fac322a435e72678885d",
           "last_updated_on": null,
           "created_on": "2011-03-23T13:17:02Z",
           "location": [
               "India",
               "Maharashtra",
               "Mumbai"
           ],
           "document_type": "Entity"
       }
   }
 }

The entity_backing field is the record for the entity to which the data record belongs to.

Test cases for the same look at the test_data_record_api.py file
