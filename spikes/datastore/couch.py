import couchdb

class Couch(object):

    def __init__(self, host='http://localhost:5984', db='mangrove'):
        self.server = couchdb.Server(host)
        self.db     = self.server[db]

    def store(self, doc):
        doc.store(self.db)

    def get_doc_by_id(self, id):
        return self.db[id]
