import copy
from datastore.documents.entitydocument import EntityDocument
from repository.repository import Repository

def get(uuid):
    repository = Repository()
    entity_doc = repository.load(uuid,EntityDocument)
    e = Entity(entity_doc.name,entity_doc.entity_type)
    e._setDocument(entity_doc)
    return e

def get_entities(uuid_list):
    entity_list=[]
    for uuid in uuid_list:
        entity_list.append(get(uuid))
    return entity_list

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

class Entity(object):

    def __init__(self,name,entity_type,location=None,attributes=None,repository=Repository()):
        self.entity_doc = None
        self._hierarchy_tree = {}
        self.repository = repository
        self.add_hierarchy("location",location)
        self._set_attr(name,entity_type,self._hierarchy_tree,attributes)

    def save(self):
        if not self.entity_doc:
            self.entity_doc = EntityDocument(name=self.name,entity_type=self.entity_type,
                                         aggregation_trees=self._hierarchy_tree,
                                         attributes=self.attributes)

        self.repository.save(self.entity_doc)
        return self.entity_doc.id

    def add_hierarchy(self,name,value):
        if type(value) == list:
            self._hierarchy_tree[name] = list(value)
        

    def _setDocument(self, entity_doc):
        self.entity_doc = entity_doc
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
