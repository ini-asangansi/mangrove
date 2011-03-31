import datetime

from couchdb.http import ResourceNotFound
from couchdb import Server
from couchdb.mapping import DateTimeField

DATABASE_NAME = 'mangrove'
SERVER_HOST = 'http://0.0.0.0:5984'

#FIXME: Duplicated it for the sake of the spike
class DataBaseBackend(object):

    def __init__(self, server=SERVER_HOST, database_name = DATABASE_NAME, *args, **kwargs):
        self.url = server
        self.server = Server(self.url)
        try:
            self.database = self.server[database_name]
        except ResourceNotFound:
            self.database = self.server.create(database_name)
        
    def save_datarecord(self, data, obj):
        data['created_at'] = DateTimeField()._to_json(datetime.datetime.now())
        data['reported_at'] = DateTimeField()._to_json(obj.reported_at)
        uuid, rev_id = self.database.save(data)
        setattr(obj, "uuid", uuid)
        return obj

    def save_entity(self, obj):
        created_at = DateTimeField()._to_json(datetime.datetime.now())
        setattr(obj, 'created_at', created_at)
        uuid, rev_id = self.database.save(obj.__dict__)
        setattr(obj, "uuid", uuid)
        return obj
        
    def get(self, uuid):
        return self.database[uuid]
        
    def __unicode__(self):
        return u"Connected on %s - working on %s" % (self.url, self.database_name)

    def __str__(self):
        return unicode(self)

    def __repr__(self):
        return repr(self.database)
