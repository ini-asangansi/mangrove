import copy
from couchdb.mapping import Document
from datastore.documents.entitydocument import EntityDocument
from repository.repository import Repository



def get(uuid):
    repository = Repository()
    entity_doc = repository.load(uuid,EntityDocument)
    e = Entity(entity_doc.name,entity_doc.entity_type)
    e._setDocument(entity_doc)
    return e

class Entity(object):

    def __init__(self,name,entity_type,location=None,attributes={},repository=Repository(),id=None):

        self.entity_doc = None
        self._hierarchy_tree = {}
        self.repository = repository
        self.add_hierarchy("location",location)
        self._set_attr(id,name,entity_type,self._hierarchy_tree,attributes)

    def save(self):
        if not self.entity_doc:
            self.entity_doc = EntityDocument(name=self.name,entity_type=self.entity_type,
                                         aggregation_trees=self._hierarchy_tree,
                                         attributes=self.attributes)

        self.repository.save(self.entity_doc)
        return self.entity_doc.id

    def add_hierarchy(self,name,value):
        if (type(value) == list):
            self._hierarchy_tree[name] = list(value)
        

    def _setDocument(self, entity_doc):
        self.entity_doc = entity_doc
        self._set_attr(entity_doc.id,entity_doc.name,entity_doc.entity_type,
                       entity_doc.aggregation_trees,entity_doc.attributes)

    def _set_attr(self, id, name,entity_type, hierarchy_tree, attributes):
        self.id = id
        self.name = name
        self.entity_type = entity_type
        self._hierarchy_tree = hierarchy_tree
        self.attributes = attributes

    @property
    def hierarchy_tree(self):
        return copy.deepcopy(self._hierarchy_tree)
