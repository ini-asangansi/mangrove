import couchdb

class DataStore(object):

    def __init__(self, host='http://localhost:5984', db='mangrove'):
        self.server = couchdb.Server(host)
        self.db     = self.server[db]

    def store(self, doc):
        doc.store(self.db)
