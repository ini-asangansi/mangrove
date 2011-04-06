from datastore.documents import DocumentBase
from datastore.entity import Entity
from datastore.database import DatabaseManager
from services.settings import *

class TestDatabaseManager:

    def setup(self):
        database = 'test_connection'
        self.database_manager = DatabaseManager(server=SERVER, database=database)

    def teardown(self):
        if self.database_manager and self.database_manager.database :
            self.database_manager.server.delete(self.database_manager.database)

    def test_should_create_database_if_it_does_not_exist(self):
        database = 'test_connection'
        self.database_manager = DatabaseManager(server=SERVER, database=database)
        assert self.database_manager.url == SERVER
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
        database = 'test_connection'
        database_manager = DatabaseManager(server=SERVER, database=database)
        user = database_manager.load('',Entity)
        assert not user
