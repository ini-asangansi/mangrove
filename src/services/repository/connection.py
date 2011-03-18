from couchdb.http import ResourceNotFound
from services.repository.server import Server

from services.settings import *

class Connection(object):
    """
        Connect to CouchDb according to params in the settings.py file
        and store that internally.

        Access is made with this class cause it's a singleton.
    """

    def __init__(self, server=None, database=None,  *args, **kwargs):
        """
            Connect to the CouchDB server. If no database name is given , use the name provided in the settings
        """
        self.url = server or SERVER
        self.database_name = database or DATABASE

        self.server = Server(self.url)

        try:
            self.database = self.server[self.database_name]
        except ResourceNotFound:
            self.database = self.server.create(self.database_name)

    def __unicode__(self):
        return u"Connected on %s - working on %s" % (self.url, self.database_name)

    def __str__(self):
        return unicode(self)

    def __repr__(self):
        return repr(self.database)
  