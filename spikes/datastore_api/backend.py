import datetime

from couchdb.http import ResourceNotFound
from couchdb import Server
from couchdb.mapping import DateTimeField

DATABASE_NAME = 'mangrove'
SERVER_HOST = 'http://0.0.0.0:5984'

#FIXME: Duplicated it for the sake of the spike
class DataBaseBackend(object):
    """
        Connect to CouchDb according to params in the settings.py file
        and store that internally.

        Access is made with this class cause it's a singleton.
    """

    def __init__(self, server=SERVER_HOST, database_name = DATABASE_NAME, *args, **kwargs):
        """
            Connect to the CouchDB server. If no database name is given , use the name provided in the settings
        """
        self.url = server
        self.server = Server(self.url)
        try:
            self.database = self.server[database_name]
        except ResourceNotFound:
            self.database = self.server.create(database_name)
        
    def save_datarecord(self, data, obj):
        data['created_at'] = DateTimeField()._to_json(datetime.datetime.now())
        uuid, rev_id = self.database.save(data)
        setattr(obj, "uuid", uuid)
        return obj

    def save_entity(self, obj):
        created_at = DateTimeField()._to_json(datetime.datetime.now())
        uuid, rev_id = self.database.save({'geocode' : obj.geocode, 'geoname' :obj.geoname, 'unique_name' :obj.unique_name, 'created_at' :created_at })
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
