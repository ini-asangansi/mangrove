#
# Entity class is main way of interacting with Entities AND datarecords.
# Datarecords are always submitted/retrieved from an Entity
#

import datetime

from backend import DataBaseBackend

class DataRecord(object):

    def __init__(self, for_entity_uuid, record_dict, reported_at):
        setattr(self, 'for_entity_uuid', for_entity_uuid)
        setattr(self, 'reported_at', reported_at)
        setattr(self, 'data', record_dict)

    def save(self):
        return DataBaseBackend().save_datarecord(self.data, self)

class Entity(object):
    
    def __init__(self, geocode = None, geoname = None, unique_name = None, aggregation_tree = None):
        data = {'geocode' : geocode, 'geoname' :geoname, 'unique_name' :unique_name, 'aggregation_tree' :aggregation_tree}
        for key, value in data.items():
            setattr(self, key, value)
                
    def save(self):
        return DataBaseBackend().save_entity(self)
        
    def submit_datarecord(self, record_dict, created_at):
        data_record = DataRecord(self.uuid, record_dict, created_at)
        return data_record

        
    def update_datarecord(self,uid,record_dict):
        self.invalidate_datarecord(uid)
        return self.submit_datarecord(record_dict, datetime.datetime.now())

    def invalidate_datarecord(self,uid):
        pass

    def revalidate_datarecord(self,uid):
        pass


    def current_state(self):
        return self.state(None)

    def state(self, asof=None):
        pass
