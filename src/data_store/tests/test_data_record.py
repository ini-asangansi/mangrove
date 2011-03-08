import couchdb

__author__ = 'apgeorge'

from nose.tools import *

from couchdb import Server

#Given a python data_record, store the same in couchdb as a json doc.

class   TestDataRecord:

    def setup(self):
        self.server = Server()
        try:
            DATA_STORE = 'data_store'
            self.db = self.server[DATA_STORE]
        except couchdb.http.ResourceNotFound:
            self.db = self.server.create(DATA_STORE)

    def test_save_new_data_record(self):
        assert_is_not_none(self.db)
        

            