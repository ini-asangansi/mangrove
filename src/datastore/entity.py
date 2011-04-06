import copy
from datetime import datetime, date
from datastore.documents.entitydocument import EntityDocument
from databasemanager.database_manager import DatabaseManager
from datastore.documents.datarecorddocument import DataRecordDocument
from datastore import config


_view_names = { "latest" : "by_values" }

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

    def __init__(self,name,entity_type = None,location=None):
        self._entity_doc = None
        self._hierarchy_tree = {}
        self._database_manager = DatabaseManager(server=config._server,database=config._db)
        self.add_hierarchy("location",location)
        self._set_attr(name,entity_type,self._hierarchy_tree)

    def save(self):
        if not self._entity_doc:
            # create the document to be persisted to CouchDb
            self._entity_doc = EntityDocument(name=self.name,entity_type=self.entity_type,
                                         aggregation_trees=self._hierarchy_tree
                                         )

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
#        reporter = get(reported_by)
        attributes = {}
        for key in data_record:
            val = data_record[key]
            if type(val)==tuple:
                value,meta = val
                attributes[key] = {"value": value,"metadata" : meta}
            else:
                attributes[key] = {"value":val}

        data_record_doc = DataRecordDocument(entity = self._entity_doc, reporter = reported_by._entity_doc,
                                             source = source, _reported_on = reported_on, _attributes=attributes)
        self._database_manager.save(data_record_doc)
        return data_record_doc.id

    def _setDocument(self, entity_doc):
        self._entity_doc = entity_doc
        self._set_attr(entity_doc.name,entity_doc.entity_type,
                       entity_doc.aggregation_trees)

    def _set_attr(self, name,entity_type, hierarchy_tree):
        self.name = name
        self.entity_type = entity_type
        self._hierarchy_tree = hierarchy_tree

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

    def values(self, aggregation_rules, asof = None):
        """
        returns the aggregated value for the given fields using the aggregation function specified for data collected till a point in time.
         Eg: data_records_func = {'arv':'latest', 'num_patients':'sum'} will return latest value for ARV and sum of number of patients
        """
        asof = asof or datetime.now()
        result = {}
        
        for field,aggregate_fn in aggregation_rules.items():
            view_name = self._translate(aggregate_fn)
            result[field] = self._get_aggregate_value(field,view_name,asof)
        return result


    def _get_aggregate_value(self, field, aggregate_fn,date):
        entity_id = self._entity_doc.id
        rows = self._database_manager.load_all_rows_in_view('mangrove_views/'+aggregate_fn, group_level=2,descending=False,
                                                     startkey=[self.entity_type, entity_id],
                                                     endkey=[self.entity_type, entity_id, date.year, date.month, date.day, {}])
        # The above will return rows in the format described:
        # Row key=['clinic', 'e4540e0ae93042f4b583b54b6fa7d77a'],
        #   value={'beds': {'timestamp_for_view': 1420070400000, 'value': '15'},
        #           'entity_id': {'value': 'e4540e0ae93042f4b583b54b6fa7d77a'}, 'document_type': {'value': 'Entity'},
        #           'arv': {'timestamp_for_view': 1420070400000, 'value': '100'}, 'entity_type': {'value': 'clinic'}
        #           }
        #  The aggregation map-reduce view will return only one row for an entity-id
        # From this we return the field we are interested in.
        return rows[0]['value'][field]['value'] if len(rows) else None

    def _translate(self, aggregate_fn):
        return _view_names.get(aggregate_fn) or aggregate_fn





    




    
