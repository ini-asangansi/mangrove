from datastore.documents import DocumentBase
from datastore.entity import Entity
from datastore.database import get_db_manager, _delete_db_and_remove_db_manager
from services.settings import *

class TestDatabaseManager:

    def setup(self):
        self.database_manager = get_db_manager('http://localhost:5984/', 'mangrove-test')

    def teardown(self):
        _delete_db_and_remove_db_manager(self.database_manager)

    def test_should_create_database_if_it_does_not_exist(self):
        _delete_db_and_remove_db_manager(self.database_manager)
        server = 'http://localhost:5984/'
        database = 'mangrove-test'
        self.database_manager = get_db_manager(server, database)
        assert self.database_manager.url == server
        assert self.database_manager.database_name == database
        assert self.database_manager.server
        assert self.database_manager.database

    def test_should_persist_and_load_document_to_database(self):
        document = DocumentBase(document_type='TestDocument')

        document = self.database_manager.save(document)
        assert document.document_type == 'TestDocument'

        document1 = self.database_manager.load(document.id)
        assert document1

    def test_should_return_none_if_documentid_is_empty(self):
        user = self.database_manager.load('',Entity)
        assert not user
