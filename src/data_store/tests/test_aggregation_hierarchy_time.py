from datetime import datetime
import couchdb
from couchdb.client import Server
from couchdb.design import ViewDefinition
from couchdb.mapping import Document, IntegerField, TextField, DateTimeField, Field, ListField, DictField, DictField, Mapping, Mapping
from nose.tools import *
from src.data_record.data_record import DataRecord2, IntDataRecord2, DateTimeDataRecord2, FloatDataRecord2
from src.couch_http_wrapper import CouchHttpWrapper

class TestHierarchyAndTimeAggregate:

    DATA_STORE = 'data_store4'
    def setup(self):
        self.server = Server()
        try:
            self.db = self.server[DATA_STORE]
        except couchdb.http.ResourceNotFound:
            self.db = self.server.create(DATA_STORE)
            self.create_testdata_by_httpAPI()
            self.create_views()

    def create_testdata_by_httpAPI(self):
        httpwrapper = CouchHttpWrapper('localhost', '5984')

        fp = open("/Users/mukeshkumar/mangrove/src/data_store/tests/test_data/test_data.json")
        docs= fp.read()
        httpwrapper.saveBulkDoc(self.DATA_STORE,docs)

    def create_views(self):
        view = ViewDefinition('by_field','by_field','''
         function(doc){for(i in doc.attr){
            field_dict = doc.attr[i];
            if (field_dict.type == "Number")
                emit(field_dict.field,parseInt(field_dict.value));
         }}''','''_sum''')
        view.sync(self.db)
        view = ViewDefinition('by_location','by_location','''function(doc) {
                                for(i in doc.attr){
                                    field_dict = doc.attr[i];
                                    if (field_dict.type == "Number"){
                                        key = [doc.namespace, field_dict.field];
                                        for (v in doc.location){
                                            key.push(doc.location[v]);
                                        }
                                    key.push(field_dict.timestamp);
                                    emit(key,parseInt(field_dict.value));
                                    }
                                }
                                }''','''_count'''
                              )
        view.sync(self.db)
    def test_db_created(self):
        assert True
#    def test_total_for_Maharashtra_in_Feb_is_hundred(self):
#        number_of_patients = self.fetch_by_loc_and_time("MH",2,"month")
#        assert number_of_patients==100


