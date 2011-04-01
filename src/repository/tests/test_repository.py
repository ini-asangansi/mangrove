from datastore.entity import Entity
from repository.DocumentBase import DocumentBase
from repository.repository import Repository
from services.settings import *

class TestRepository:

    def setup(self):
        database = 'test_connection'
        self.repository = Repository(server=SERVER, database=database)

    def teardown(self):
        if self.repository and self.repository.database :
            self.repository.server.delete(self.repository.database)

    def test_should_create_database_if_it_does_not_exist(self):
        database = 'test_connection'
        self.repository = Repository(server=SERVER, database=database)
        assert self.repository.url == SERVER
        assert self.repository.database_name == database
        assert self.repository.server
        assert self.repository.database

    def test_should_persist_and_load_document_to_database(self):
        document = DocumentBase(document_type='TestDocument')

        document = self.repository.save(document)
        assert document.document_type == 'TestDocument'

        document1 = self.repository.load(document.id)
        assert document1

    def test_should_return_none_if_documentid_is_empty(self):
        database = 'test_connection'
        repository = Repository(server=SERVER, database=database)
        user = repository.load('',Entity)
        assert not user
