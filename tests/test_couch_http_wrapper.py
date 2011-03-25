import os
from couchdb.client import Server
from tests.couch_http_wrapper import CouchHttpWrapper
from nose.tools import *

class TestCouchHTTPWrapper:
    DATA_STORE = 'data_store4'

    def test_exported_data_to_couch(self):
        self.export_test_data_to_couch()
        server = Server()
        db=server[self.DATA_STORE]
        assert db['ip1']


    def export_test_data_to_couch(self):
        http_wrapper = CouchHttpWrapper('localhost', '5984')
        http_wrapper.deleteDb(self.DATA_STORE)
        http_wrapper.createDb(self.DATA_STORE)
        test_data_dir = os.path.join(os.path.dirname(__file__), 'test_data/')
        fp = open(test_data_dir + 'test_data.json')
        http_wrapper.saveBulkDoc(self.DATA_STORE, fp.read())
        fp.close()


    