from couchdb.http import ResourceNotFound
from couchdb import Server

DATABASE_NAME = 'mangrove'
SERVER_HOST = 'http://0.0.0.0:5984'

#FIXME: Duplicated it for the sake of the spike
class Connection(object):
    """
        Connect to CouchDb according to params in the settings.py file
        and store that internally.

        Access is made with this class cause it's a singleton.
    """

    def __init__(self, server=SERVER_HOST, *args, **kwargs):
        """
            Connect to the CouchDB server. If no database name is given , use the name provided in the settings
        """
        self.url = server or SERVER
        self.server = Server(self.url)
            
    def get_database(self, database_name = DATABASE_NAME):
        try:
            self.database = self.server[database_name]
        except ResourceNotFound:
            self.database = self.server.create(database_name)
        return self.database
        
    def save_entity(self, arg, entity):
        return self.get_database(DATABASE_NAME).save(arg)
        
    def get(self, uuid):
        return self.database[uuid]
        
    def __unicode__(self):
        return u"Connected on %s - working on %s" % (self.url, self.database_name)

    def __str__(self):
        return unicode(self)

    def __repr__(self):
        return repr(self.database)
