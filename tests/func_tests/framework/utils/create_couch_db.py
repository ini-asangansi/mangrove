import os
from setuptools.dist import assert_bool
from couchdb.client import Server
from tests.couch_http_wrapper import CouchHttpWrapper

class TestCouchHTTPWrapper:
    DATA_STORE = 'mangrove_web'

    def test_exported_data_to_couch(self):
        self.export_test_data_to_couch()
        server = Server()
        db=server[self.DATA_STORE]
        assert db['nogo@mail.com']

    def export_test_data_to_couch(self):
        http_wrapper = CouchHttpWrapper('localhost', '5984')
        http_wrapper.deleteDb(self.DATA_STORE)
        http_wrapper.createDb(self.DATA_STORE)
        test_data_dir = os.path.join(os.path.dirname(__file__), '../../../test_data/')
        fp = open(test_data_dir + 'functionalTestData.json')
        http_wrapper.saveBulkDoc(self.DATA_STORE, fp.read())
        fp.close()
