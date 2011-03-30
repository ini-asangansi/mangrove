from couchdb.mapping import Document
from datastore.documents.entitydocument import EntityDocument
from repository.repository import Repository

__author__ = 'shweta'

class Entity(object):

    
    def __init__(self,attributes,repository=Repository()):
        self.name = attributes["name"]
        self.entity_type = attributes["entity_type"]
        self.location = attributes["location"]
        self.repository = repository

    def save(self):
        entity_doc = EntityDocument(name=self.name,entity_type=self.entity_type,aggregation_trees={"location":self.location})
        self.repository.save(entity_doc)
        return entity_doc.id

