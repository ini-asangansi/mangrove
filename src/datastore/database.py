from couchdb.design import ViewDefinition
from couchdb.http import ResourceNotFound
from services.settings import *
from threading import Lock
from datastore import config
from documents import DocumentBase
import couchdb.client


_dbm = None

def get_db_manager():
    global _dbm
    if  _dbm is  None:
        # no dbm yet, lazily instantiate, but protect with a lock
        # and recheck so as to not do this twice
        with Lock():
            if _dbm is None:
                _dbm = DatabaseManager(server=config._server,database=config._db)

    return _dbm

class DatabaseManager:
    def __init__(self, server=None, database=None,  *args, **kwargs):
        """
            Connect to the CouchDB server. If no database name is given , use the name provided in the settings
        """
        self.url = (server if server is not None else SERVER)
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

    def load_all_rows_in_view(self,view_name,**values):
        return self.database.view(view_name,**values).rows

    def create_view(self,view_name,map,reduce, view_document='mangrove_views'):
        view = ViewDefinition(view_document,view_name,map,reduce)
        view.sync(self.database)

    def save(self, document):
        document.store(self.database)
        return document

    def delete(self, document):
        self.database.delete(document)

    def load(self, id, document_class=DocumentBase):
        if id:
            return document_class.load(self.database, id)
        return None

class Server(couchdb.client.Server):
    def delete(self, database):
        super(Server, self).delete(database.name)

class DatabaseManagerForTests(DatabaseManager):
    def delete_database(self):
        self.server.delete(self.database)

