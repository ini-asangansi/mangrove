from services.entity_management.models import Organization, Entity
from services.repository.connection import Connection
from services.repository.repository import Repository

class EntityManagementService:

    def __init__(self, repository=Repository(Connection())):
        self.repository = repository

    def create_entity(self, entity):
        saved_entity =self.repository.save(entity)
        if not self.exists_entity_type_by_location_view(saved_entity.entity_type):
               self.__create_by_location_view_for_entity_type(saved_entity.entity_type)
        if not self.exists_entity_type_by_time_view(saved_entity.entity_type):
               self.__create_by_time_view_for_entity_type(saved_entity.entity_type)
        return saved_entity

    def load_entity(self, id, entity = Entity):
        return self.repository.load(id, entity)

    def update_entity(self, entity):
        return self.repository.save(entity, entity.__class__)

    def __create_by_location_view_for_entity_type(self,entity_type):

        map = """ function(doc)
                  {
                    var isNumeric = function(n)
                                    {
                                        return !isNaN(parseFloat(n)) && isFinite(n);
                            };

                    if (doc.document_type == 'DataRecord' && doc['entity_backing_field']['_data']['entity_type'] == '%s')
                    {
                        var value = {};
                        for(index in doc.attributes)
                        {
                             if(isNumeric(doc.attributes[index]))
                             {
                                 value[index] = parseFloat(doc.attributes[index]);
                             }
                         }
                         for(index in value)
                         {
                            var key = [].concat(doc['entity_backing_field']['_data']['location']);
		                    key.splice(0,0, index);
                            emit(key  ,value[index]);                            
                         }
                     }
                  }""" % (entity_type,)
        reduce = """ _stats """
        self.repository.create_view(entity_type,"by_location",map,reduce)

    def __create_by_time_view_for_entity_type(self,entity_type):

        map = """ function(doc)
                  {
                    var isNumeric = function(n)
                                    {
                                        return !isNaN(parseFloat(n)) && isFinite(n);
                            };

                    if (doc.document_type == 'DataRecord' && doc['entity_backing_field']['_data']['entity_type'] == '%s')
                    {
                        var value = {};
                        var datePart = doc.created_on.split('-',3);
		                datePart[2] = datePart[2].substring(0,2);
                        for(index in doc.attributes)
                        {
                             if(isNumeric(doc.attributes[index]))
                             {
                                 value[index] = parseFloat(doc.attributes[index]);
                             }
                         }
                         for(index in value)
                         {
                            var key = [index, datePart[0], datePart[1], datePart[2]];
                            emit(key  ,value[index]);
                         }
                     }
                  }""" % (entity_type,)
        reduce = """ _stats """
        self.repository.create_view(entity_type,"by_time",map,reduce)

    def exists_entity_type_by_location_view(self,entity_type):
            entity_type_views = self.repository.load('_design/%s' % (entity_type,))
            if entity_type_views and entity_type_views['views'].get('by_location'):
                return True
            return False

    def exists_entity_type_by_time_view(self,entity_type):
            entity_type_views = self.repository.load('_design/%s' % (entity_type,))
            if entity_type_views and entity_type_views['views'].get('by_time'):
                return True
            return False