'''
An example of a high-level API for manipulating Entities and Data Records.
'''

import uuid

#
# Module Functions
#

'''
I prefer to use module level functions over @classmethod and @staticmethod to play to
play the role of 'Static' or 'Class' methods  because @classmethod and @staticmethod
are confusing and can have unexpected behavior.

In particular, @classmethod is NOT a C++ or ObjC class method, it is in fact a meta-programming
construct for dynamically manipulating Classes usually to create Factories.

@staticmethod is more like a Java 'static' (Class method) but it is nothing more than a module
function declared within a Class definition, it buys you nothing else beyond possible confusion with
@classmethod.

For this reason I prefer to keep it clean and use module functions for 'Statics'

See here for a brief discussion: http://bit.ly/el5ad6
and more in depth explanation: http://bit.ly/gQVTtB

'''

def entity_for_id(uid):
    ''' Retrieve an entity with the given UID '''
    return entities_for_ids((uid))

def entities_for_ids(uids):
    ''' return list of entities for given uids '''
    entities = []
    for uid in uids:
        try:
            entities.append(Entity(id=uid))
        except:
            # guess there wasn't an entity with that id
            pass

    return entities

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
# Entity class is main way of interacting with Entities AND datarecords.
# Datarecords are always submitted/retrieved from an Entity
#

class Entity(object):
    # entity creation / retrieval
    def __init__(self, arg=None):
        '''
        arg is either a uuid, in which case try to instantiate out of DB.
        OR arg is a dict, in which case create a new one

        '''

        if arg is None or type(arg) not in (dict,uuid.UUID):
            raise ValueError('Entity must be created with UUID or dictionary')

        if type(arg) == uuid.UUID:
            # retrieve from DB
            pass
        else:
            # create new entity with a new datarecord containing the
            # attributes in the arg dict
            pass

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
    