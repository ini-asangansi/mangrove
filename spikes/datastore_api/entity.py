#
# Entity class is main way of interacting with Entities AND datarecords.
# Datarecords are always submitted/retrieved from an Entity
#

import datetime

from backend import DataBaseBackend
from query import QueryManager

class DataRecord(object):

    #FIXME entity_uuid may not be enough for us to relate to an entity
    #But keeping it simple for now and add other stuff only when we need
    #And I don't think we need a document_type in the documents to distinguish between entities and data records
    #Because documents which have the field for_entity_uuid _will_ be datarecords, and others not. 
    #And this can work in map functions to differentiate datarecords from entities. 
    #lets keep it simple for now, unless it doesn't work
    def __init__(self, for_entity_uuid, record_dict):
        setattr(self, 'for_entity_uuid', for_entity_uuid)
        setattr(self, 'data', record_dict)

    def save(self):
        return DataBaseBackend().save_datarecord(self.data, self)

class Entity(object):
    
    # entity creation / retrieval
    def __init__(self, geocode = None, geoname = None, unique_name = None):
        '''
        arg is either a uuid, in which case try to instantiate out of DB.
        OR arg is a dict, in which case create a new one

        '''
        
        data = {'geocode' : geocode, 'geoname' :geoname, 'unique_name' :unique_name }
        for key, value in data.items():
            setattr(self, key, value)
                
    def save(self):
        return DataBaseBackend().save_entity(self)
        
    #The user has to call .save() on the datarecord after calling this api
    #Also a entity which is not persisted on the datastore and hence has no uuid, can-not be related to a datarecord.
    #Because we use the uuid of the entity to relate a datarecord to an entity
    def submit_datarecord(self, record_dict):
        '''
        Add a new datarecord to this Entity.

        Return a UUID for the datarecord.
        '''
        data_record = DataRecord(self.uuid, record_dict)
        return data_record

        
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


    # attribute retrieval (Queries)

    # Note: There are lots of options for this API. It can be custom functions like
    # I have here. They could be 'properties' to allow things like:
    #    if patient.name == 'Jeff': <do something>
    # And we could even implement the dict methods like __getitem__ __setitem__ so that we could do
    # things like:
    #
    # patient['name'] = 'Jeff'
    #

    def current_state(self):
        '''
        Returns a dict of the latest values in the entities data records.

        ex.
            >>> print patient.current_state()
            { 'type':'patient', 'weight':45, 'dob':'2011-01-12', 'muac':'10' }

        '''
        return self.state(None)

    def state(self, asof=None):
        '''
        return latest attributes as-of the given date. If 'asof' is None,
        return the absolute latest.
        '''
        pass
