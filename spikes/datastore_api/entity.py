#
# Entity class is main way of interacting with Entities AND datarecords.
# Datarecords are always submitted/retrieved from an Entity
#

from backend import DataBaseBackend
from query import QueryManager

class Entity(object):
    
    # entity creation / retrieval
    def __init__(self, geocode = None, geoname = None, unique_name = None):
        '''
        arg is either a uuid, in which case try to instantiate out of DB.
        OR arg is a dict, in which case create a new one

        '''
        
        self.data = {'geocode' : geocode, 'geoname' :geoname, 'unique_name' :unique_name }
        for key, value in self.data.items():
            setattr(self, key, value)
                
    def save(self):
        return DataBaseBackend().save(self.data, self)
        
    # datarecord CRUD
    def submit_datarecord(self, record_dict):
        '''
        Add a new datarecord to this Entity.

        Return a UUID for the datarecord.
        '''
        pass
        
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
