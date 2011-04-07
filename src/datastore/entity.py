import copy

from datetime import datetime
from documents import EntityDocument, DataRecordDocument
from database import get_db_manager
from utils import is_string, is_sequence, is_not_empty

_view_names = { "latest" : "by_values" }

def get(uuid):
    entity_doc = get_db_manager().load(uuid,EntityDocument)
    e = Entity(_document = entity_doc)
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


#
# Constants
#

# use 'classes' to group constants
class attribute_names(object):
    MODIFIED = 'modified'
    CREATED = 'created'
    EVENT_TIME = 'event_time'
    ENTITY_ID = 'entity_id'
    SUBMISSION_ID = 'submission_id'
    AGG_PATHS = 'aggregation_paths'
    GEO_PATH = '_geo'
    TYPE_PATH = '_type'
    DATA = 'data'




# Entity class is main way of interacting with Entities AND datarecords.
# Datarecords are always submitted/retrieved from an Entity




class Entity(object):
    """
        Entity class is main way of interacting with Entities AND datarecords.
    """

    def __init__(self, entity_type = None,location=None, aggregation_paths = None, _couch_document = None):
        '''Construct a new entity.

        Note: _document is used for 'protected' factory methods and
        should not be passed in standard construction.

        If _document is passed, the other args are ignored

        Key arguments:
        --  entity_type can be either a string or a sequence for hierarchical type
        --  location is a sequence of form ['us', 'ca', 'sanfrancisco']
        '''
        assert _couch_document is None or is_sequence(entity_type) or is_string(entity_type)
        assert _couch_document is None or location is None or is_sequence(location)
        assert _couch_document is None or isinstance(aggregation_paths, dict)
        assert _couch_document is None or isinstance(_couch_document, EntityDocument)

        # Are we being constructed from an existing doc?
        if _couch_document is not None:
            self._entity_doc = _couch_document
            return

        # Not made from existing doc, so create a new one
        self._entity_doc = EntityDocument()
        self.entity_type = entity_type

        # add aggregation paths
        if entity_type is not None:
            if is_string(entity_type):
                entity_type = tuple(entity_type)
            self.set_aggregation_path(attribute_names.TYPE_PATH, entity_type)

        if location is not None:
            self.set_aggregation_path(attribute_names.GEO_PATH, location)

        if aggregation_paths is not None:
            reserved_names = (attribute_names.TYPE_PATH, attribute_names.GEO_PATH)
            for name, path in aggregation_paths:
                if name in reserved_names:
                    raise ValueError('Attempted to add an aggregation path with a reserved name')
                self.set_aggregation_path(name, path)

        # TODO: why should Entities just be saved on init??

    @property
    def id(self):
        return self._entity_doc.id if self._entity_doc is not None else None

    def save(self):
        '''Save the entity to the DB and return UUID'''
        assert self._entity_doc is not None and self._entity_doc.id is not None
        return get_db_manager().save(self._entity_doc)

    def set_aggregation_path(self, name, path):
        assert self._entity_doc is not None
        assert is_string(name) and is_not_empty(name)
        assert is_sequence(path) and is_not_empty(path)

        assert isinstance(self._entity_doc[attribute_names.AGG_PATHS], dict)
        self._entity_doc[attribute_names.AGG_PATHS][name]=path

        # TODO: Depending on implementation we will need to update aggregation paths
        # on data records--in which case we need to set a dirty flag and handle this
        # in save
        #
    def add_hierarchy(self,name,value):
        if type(value) == list:
            self._hierarchy_tree[name] = list(value)

    def submit_data_record(self, data_record, reported_on = None, submission_id = None):
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
        # reporter = get(reported_by)
        attributes = {}
        for key in data_record:
            val = data_record[key]
            if type(val)==tuple:
                value,meta = val
                attributes[key] = {"value": value,"metadata" : meta}
            else:
                attributes[key] = {"value":val}

        data_record_doc = DataRecordDocument(entity = self._entity_doc,
                                             attributes = attributes,
                                             reported_on = reported_on,
                                             submission_id = submission_id)
        get_db_manager().save(data_record_doc)
        return data_record_doc.id

    def _set_attr(self, entity_type, hierarchy_tree = None):
        self.entity_type = entity_type
        self._hierarchy_tree = hierarchy_tree or {}

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
        return self.submit_data_record(record_dict)
  	 	
  	 	
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
        rows = get_db_manager().load_all_rows_in_view('mangrove_views/'+aggregate_fn, group_level=2,descending=False,
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





    




    
