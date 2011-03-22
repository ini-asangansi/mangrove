from services.repository.DocumentBase import DocumentBase
from services.repository.connection import Connection
from services.repository.repository import Repository
from services.settings import *

class TestConnection:

    def test_should_create_database_if_it_does_not_exist(self):
        database = 'test_connection'
        self.connection = Connection(server=SERVER, database=database)
        assert self.connection.url == SERVER
        assert self.connection.database_name == database
        assert self.connection.server
        assert self.connection.database

    def teardown(self):
        if self.connection and self.connection.database :
            self.connection.server.delete(self.connection.database)

class TestRepository:

    def setup(self):
        database = 'test_connection'
        self.connection = Connection(server=SERVER, database=database)

    def teardown(self):
        if self.connection and self.connection.database :
            self.connection.server.delete(self.connection.database)

    def test_should_persist_and_load_document_to_database(self):
        document = DocumentBase(document_type='TestDocument')
        repository = Repository(connection=self.connection)
        document = repository.save(document)
        assert document.document_type == 'TestDocument'

        document1 = repository.load(document.id)
        assert document1

