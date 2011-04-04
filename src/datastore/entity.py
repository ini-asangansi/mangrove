import copy
from datastore.documents.entitydocument import EntityDocument
from databasemanager.database_manager import DatabaseManager
from datastore.documents.datarecorddocument import DataRecordDocument
from datastore import config

def get(uuid):
    database_manager = DatabaseManager(server=config._server,database=config._db)
    entity_doc = database_manager.load(uuid,EntityDocument)
    e = Entity(entity_doc.name,entity_doc.entity_type)
    e._setDocument(entity_doc)
    return e

def get_entities(uuids):
    return [ get(i) for i in uuids ]

def entities_for_attributes(attrs):
    '''
    retrieve entities with datarecords with the given
    named attributes. Can be used to search for entities
    by identifying info like a phone number

    Include 'type' as an attr to restrict to a given entity type

    returns a sequence of 0, 1 or more matches

    ex:
    attrs = { 'type':'clinic', 'name': 'HIV Clinic' }
    print entities_for_attributes(attrs)

    '''

    pass

# geo aggregation specific calls
def entities_near(geocode, radius=1, attrs=None):
    '''
    Retrieve an entity within the given radius (in kilometers) of
    the given geocode that matches the given attrs

    Include 'type' as an attr to restrict to a given entity type

    returns a sequence

    '''
    pass

def entities_in(geoname, attrs=None):
    '''
    Retrieve an entity within the given fully-qualified geographic
    placename.

    Include 'type' as an attr to restrict to a given entity type

    returns a sequence

    ex.
    found = entities_in(
    [us,ca,sanfrancisco],
    {'type':'patient', 'phone':'4155551212'}
    )

    '''
    pass


# Entity class is main way of interacting with Entities AND datarecords.
# Datarecords are always submitted/retrieved from an Entity


class Entity(object):
    """
        Entity class is main way of interacting with Entities AND datarecords.
    """

    def __init__(self,name,entity_type,location=None,attributes=None):
        self._entity_doc = None
        self._hierarchy_tree = {}
        self._database_manager = DatabaseManager(server=config._server,database=config._db)
        self.add_hierarchy("location",location)
        self._set_attr(name,entity_type,self._hierarchy_tree,attributes)

    def save(self):
        if not self._entity_doc:
            # create the document to be persisted to CouchDb
            self._entity_doc = EntityDocument(name=self.name,entity_type=self.entity_type,
                                         aggregation_trees=self._hierarchy_tree,
                                         attributes=self.attributes)

        self._database_manager.save(self._entity_doc)
        return self._entity_doc.id

    def add_hierarchy(self,name,value):
        if type(value) == list:
            self._hierarchy_tree[name] = list(value)

    def submit_data_record(self,data_record,reported_on,reported_by = None, source = None):
        """
            Add a new datarecord to this Entity.
            Return a UUID for the datarecord.

            data_record is a dictionary in the below format,

            Dictionary Field: Field Name
            Dictionary Value: The value or a two tuple of (value, dictionary of meta information).

            E.g.
                Simple key value pairs: {"beds" : 10,"meds" : 20, "doctors":2}
                Additional meta information : {"meds":(10,{"expiry_date":12/7/1988,"brand":"abc"})}
                Both: { "beds" : 10, "medicines" : (10,{"notes":"recorded by mr xyz"}) }

            We store this in couch as

             attributes:{
                            "beds":{
                                    "value":10
                            }
                            "medicines":{
                                        "value":10,
                                        "metadata":{
                                                "notes":"recorded by mr xyz"
                                        }
                            }
             }
        """
        if not self._entity_doc:
            print "you cannot submit a datarecord without saving the entity" # TODO: Handle validation
            return None
        reporter = get(reported_by)
        attributes = {}
        for key in data_record:
            val = data_record[key]
            if type(val)==tuple:
                value,meta = val
                attributes[key] = {"value": value,"metadata" : meta}
            else:
                attributes[key] = {"value":val}

        data_record_doc = DataRecordDocument(entity = self._entity_doc, reporter = reporter._entity_doc,
                                             source = source, _reported_on = reported_on, _attributes=attributes)
        self._database_manager.save(data_record_doc)
        return data_record_doc.id

    def _setDocument(self, entity_doc):
        self._entity_doc = entity_doc
        self._set_attr(entity_doc.name,entity_doc.entity_type,
                       entity_doc.aggregation_trees,entity_doc.attributes)

    def _set_attr(self, name,entity_type, hierarchy_tree, attributes):
        self.name = name
        self.entity_type = entity_type
        self._hierarchy_tree = hierarchy_tree
        self.attributes = attributes or {}

    @property
    def hierarchy_tree(self):
        return copy.deepcopy(self._hierarchy_tree)


    # Note: The below has not been implemented yet.

    def update_datarecord(self,uid,record_dict):
        '''
        Invalidates the record identified by the passed 'uid'
  	 	
        and creates a new one using the record_dict.
  	 	
  	 	
        This can be used to _correct_ bad submissions.
  	 	
  	 	
        Returns uid of new corrected record

  	 	
        '''
  	 	
        self.invalidate_datarecord(uid)
  	 	
        return self.submit_datarecord(record_dict)
  	 	
  	 	
    def invalidate_datarecord(self,uid):
  	 	
        '''
  	 	
        Mark datarecord identified by uid as 'invalid'
  	 	
  	 	
        Can be used to mark a submitted record as 'bad' so that

  	 	
        it will be ignored in reporting. This is because we

  	 	
        don't want to delete submitted data, even if it is

  	 	
        erroneous.
  	 	
        '''
  	 	
        pass

  	 	
  	 	
    def revalidate_datarecord(self,uid):
  	 	
        '''
  	 	
        Sometimes we make mistakes and the data we thought was bad is

  	 	
        good. This lets us reverse an invalidation.
  	 	
        '''
        pass

    
    def current_state(self):
  	 	
        '''
  	 	
        Returns a dict of the latest values in the entities data records.
  	 	
  	 	
        ex.
  	 	
            >>> print patient.current_state()
  	 	
            { 'type':'patient', 'weight':, 'dob':'--', 'muac':'' }
  	 	
  	 	
        '''
  	 	
        return self.state(None)
  	 	
  	 	
    def state(self, asof=None):
  	 	
        '''

        return latest attributes as-of the given date. If 'asof' is None,
  	 	
        return the absolute latest.
  	 	
        '''
  	 	
        pass

    
