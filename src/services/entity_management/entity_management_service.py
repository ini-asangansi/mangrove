from services.entity_management.models import Organization, Entity
from services.repository.connection import Connection
from services.repository.repository import Repository

class EntityManagementService(object):

    def __init__(self, repository=Repository(Connection())):
        self.repository = repository

    def create_entity(self, entity):
        saved_entity =self.repository.save(entity)
        if not self.exists_entity_type_view(saved_entity.entity_type, 'by_location'):
               self.__create_by_location_view_for_entity_type(saved_entity.entity_type)
        if not self.exists_entity_type_view(saved_entity.entity_type, 'by_time'):
               self.__create_by_time_view_for_entity_type(saved_entity.entity_type)
        if not self.exists_entity_type_view(saved_entity.entity_type, 'current_values'):
               self.__create_current_values_view_for_entity_type(saved_entity.entity_type)
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
                   var isNotNull = function(o)
                   {
                        return !((o === undefined) || (o == null));
                   };
                   if (doc.document_type == 'DataRecord' && isNotNull(doc.entity_backing_field) && doc.entity_backing_field.entity_type == '%s')
                   {
                       var value = {};
                       var date = new Date(doc.created_on);
                       var aggregation_trees = doc.entity_backing_field.aggregation_trees || {};
                       for(index in doc.attributes)
                       {
                            if(isNotNull(doc.attributes[index]) && isNotNull(doc.attributes[index]['value']) && isNumeric(doc.attributes[index]['value']))
                            {
                                value[index] = parseFloat(doc.attributes[index]['value']);
                            }
                        }
                        for(index in value)
                        {
                           for(hierarchy in aggregation_trees)
                           {
                               var key = [hierarchy].concat(aggregation_trees[hierarchy], [date.getFullYear(), date.getMonth(), date.getDate(), date.getHours(), date.getMinutes(), date.getSeconds()]);
                               key.splice(0,0, index);
                               emit(key ,value[index]);
                           }
                        }
                    }
                 }""" % (entity_type,)
        reduce = """ _stats """
        self.repository.create_view(entity_type,"by_location",map,reduce)

    def __create_by_time_view_for_entity_type(self,entity_type):

        map = """  function(doc)
                  {
                    var isNumeric = function(n)
                    {
                        return !isNaN(parseFloat(n)) && isFinite(n);
                    };
                    var isNotNull = function(o)
                    {
                        return !((o === undefined) || (o == null));
                    };
                    if (doc.document_type == 'DataRecord' && isNotNull(doc.entity_backing_field) && doc.entity_backing_field.entity_type == '%s')
                    {
                        var value = {};
                        var date = new Date(doc.created_on);
                        for(index in doc.attributes)
                        {
			            if(isNotNull(doc.attributes[index]) && isNotNull(doc.attributes[index].value) && isNumeric(doc.attributes[index].value))
                        {
                            value[index] = parseFloat(doc.attributes[index].value);
                        }
                     }
			         for(index in value)
                         {
                            var key = [index, date.getFullYear(), date.getMonth(), date.getDate(), date.getHours(), date.getMinutes(), date.getSeconds()];
                            emit(key, value[index]);
                         }
                     }
                  }""" % (entity_type,)
        reduce = """ _stats """
        self.repository.create_view(entity_type,"by_time",map,reduce)

    def __create_current_values_view_for_entity_type(self,entity_type):
        map = """  function(doc)
                 {
                    var isNotNull = function(o)
                    {
                        return !((o === undefined) || (o == null));
                    };
                    if (doc.document_type == 'DataRecord' && isNotNull(doc.entity_backing_field) && doc.entity_backing_field['entity_type'] == '%s')
                    {
                        var value = {};
                        var date = new Date(doc.created_on);
                        if(isNotNull(doc.entity_backing_field) && isNotNull(doc.entity_backing_field.attributes))
                        {
                            var attributes = doc.entity_backing_field.attributes;
                            for(index in attributes)
                            {
                                 if(isNotNull(attributes[index]) && isNotNull(attributes[index]['value']))
                                 {
                                      var attribute_object = attributes[index];
                                      attribute_object['timestamp_for_view'] = date.getTime();
                                      value[index] = attributes[index];
                                 }
                            }
                        }
                        for(index in doc.attributes)
                        {
                             var attributes = doc.attributes;
                             if(isNotNull(attributes[index]) && isNotNull(attributes[index]['value']))
                             {
                                 var attribute_object = attributes[index];
                                 attribute_object['timestamp_for_view'] = date.getTime();
                                 value[index] = attributes[index];
                             }
                         }
                         var key = [doc.entity_backing_field._id, date.getFullYear(), date.getMonth(), date.getDate(), date.getHours(), date.getMinutes(), date.getSeconds()];
                         emit (key, value);
                     }
                }""" % (entity_type,)
        reduce = """function(key, values, rereduce){
                            var isNull = function(o)
                            {
                                return (o === undefined) || (o == null);
                            };

                            var current = {entity_id : key[0][0][0]};

                            for(value in values)
                            {
                                for(index in values[value])
                                {
                                    if(isNull(current[index]) || values[value][index].timestamp_for_view > current[index].timestamp_for_view)
                                    {
                                        current[index] = values[value][index];
                                    }
                                }
                            }
                            return current;
                    }"""
        self.repository.create_view(entity_type,"current_values",map,reduce)

    def exists_entity_type_view(self,entity_type, aggregation):
            entity_type_views = self.repository.load('_design/%s' % (entity_type,))
            if entity_type_views and entity_type_views['views'].get(aggregation):
                return True
            return False