import os
from services.entity_management.models import  Entity
from services.repository.connection import Connection
from services.repository.repository import Repository

file_path = os.path.dirname(__file__)

class EntityManagementService:

    def __init__(self, repository=Repository(Connection())):
        self.repository = repository

    def create_views(self):
        if not self.exists_view('by_location'):
               self.__create_by_location_view()
        if not self.exists_view('by_time'):
               self.__create_by_time_view()
        if not self.exists_view('current_values'):
               self.__create_current_values_view()

    def create_entity(self, entity):
        saved_entity =self.repository.save(entity)
        return saved_entity

    def load_entity(self, id, entity = Entity):
        loaded_entities = self.load_entities([id], entity)
        return  loaded_entities[0]

    def load_attributes_for_entity(self, entity_id):
        rows = self.repository.load_all_rows_in_view('mangrove_views/current_values',group=True, group_level=2)
        for row in rows:
            if row['value']['entity_id']['value'] == entity_id:
                return row['value']
        return None

    def load_attributes_for_entity_as_on(self, entity_id, date):
        entity = self.load_entity(entity_id)
        rows = self.repository.load_all_rows_in_view('mangrove_views/current_values', group_level=2,descending=False,startkey=[entity.entity_type, entity_id], endkey=[entity.entity_type, entity_id, date.year, date.month, date.day, {}])
        for row in rows:
            if row['value']['entity_id']['value'] == entity_id:
                return row['value']
        return None

    def load_entities_which_have_attributes(self, attributes):
        rows = self.repository.load_all_rows_in_view('mangrove_views/current_values',group=True, group_level=2)
        for row in rows:
            match = True
            for attr in attributes:
                if not row['value'].get(attr) or not str(attributes[attr]) == row['value'][attr].get('value'):
                    match = False
            if match:
                yield row['value']

    def load_entities(self, ids = None, entity = Entity):
        if not isinstance(ids, list):
            raise TypeError('ids was expected to be of type list.')
        entities = []
        for id in ids:
            loaded_entity = self.repository.load(id, entity)
            entities.append(loaded_entity)
        return entities

    def update_entity(self, entity):
        return self.repository.save(entity, entity.__class__)

    def __create_by_location_view(self):
        path = file_path+"/CouchViews/map_by_location.js"
        map = """""".join(["%s"% line for line in open(path).readlines()])
        path = file_path+"/CouchViews/reduce_by_location.js"
        reduce = """""".join(["%s"% line for line in open(path).readlines()])
        self.repository.create_view("by_location",map,reduce)

    def __create_by_time_view(self):
        path = file_path+"/CouchViews/map_by_time.js"
        map = """""".join(["%s"% line for line in open(path).readlines()])
        path = file_path+"/CouchViews/reduce_by_time.js"
        reduce = """""".join(["%s"% line for line in open(path).readlines()])
        self.repository.create_view("by_time",map,reduce)

    def __create_current_values_view(self):
        path = file_path+"/CouchViews/map_current_values.js"
        map = """  """.join(["%s"% line for line in open(path).readlines()])
        path = file_path+"/CouchViews/reduce_current_values.js"
        reduce = """  """.join(["%s"% line for line in open(path).readlines()])
        self.repository.create_view("current_values",map,reduce)

    def exists_view(self, aggregation):
            entity_type_views = self.repository.load('_design/mangrove_views')
            if entity_type_views and entity_type_views['views'].get(aggregation):
                return True
            return False