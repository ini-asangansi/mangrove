from services.entity_management.models import  Entity
from services.repository.connection import Connection
from services.repository.repository import Repository

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
            if row['value']['entity_id'] == entity_id:
                return row['value']
        return None

    def load_attributes_for_entity_as_on(self, entity_id, date):
        rows = self.repository.load_all_rows_in_view('mangrove_views/current_values',group=True, group_level=10, startkey=[entity_id], endkey=[entity_id, date.year, date.month, date.day, {}])
        for row in rows:
            if row['value']['entity_id'] == entity_id:
                return row['value']
        return None


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
                   if (doc.document_type == 'DataRecord' && isNotNull(doc.entity_backing_field))
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
                               var key = [index].concat([hierarchy], aggregation_trees[hierarchy], [date.getFullYear(), date.getMonth(), date.getDate(), date.getHours(), date.getMinutes(), date.getSeconds()]);
                               key.splice(0,0, doc.entity_backing_field.entity_type);
                               emit(key ,value[index]);
                           }
                        }
                    }
                 }"""
        reduce = """ _stats """
        self.repository.create_view("by_location",map,reduce)

    def __create_by_time_view(self):

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
                    if (doc.document_type == 'DataRecord' && isNotNull(doc.entity_backing_field))
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
                            var key = [doc.entity_backing_field.entity_type, index, date.getFullYear(), date.getMonth(), date.getDate(), date.getHours(), date.getMinutes(), date.getSeconds()];
                            emit(key, value[index]);
                         }
                     }
                  }"""
        reduce = """ _stats """
        self.repository.create_view("by_time",map,reduce)

    def __create_current_values_view(self):
        map = """  function(doc)
                 {
                    var isNotNull = function(o)
                    {
                        return !((o === undefined) || (o == null));
                    };
                    if (doc.document_type == 'DataRecord' && isNotNull(doc.entity_backing_field))
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
                         var key = [doc.entity_backing_field.entity_type, doc.entity_backing_field._id, date.getFullYear(), date.getMonth(), date.getDate(), date.getHours(), date.getMinutes(), date.getSeconds()];
                         emit (key, value);
                     }
                }"""
        reduce = """function(key, values, rereduce){
                            var isNull = function(o)
                            {
                                return (o === undefined) || (o == null);
                            };

                            var current = {entity_id : key[0][0][1]};

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
        self.repository.create_view("current_values",map,reduce)

    def exists_view(self, aggregation):
            entity_type_views = self.repository.load('_design/mangrove_views')
            if entity_type_views and entity_type_views['views'].get(aggregation):
                return True
            return False