from datastore_api.entity import Entity
from datastore_api.connection import Connection

database = Connection().get_database()

def get(uuid):
    data_dict = database[uuid]
    entity = Entity(geocode = data_dict['geocode'], geoname = data_dict['geoname'], unique_name = data_dict['unique_name'])
    setattr(entity, 'uuid', data_dict['_id'])
    return entity
    
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
