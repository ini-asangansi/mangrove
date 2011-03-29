from services.repository.DocumentBase import DocumentBase
from services.repository.connection import Connection
from services.repository.repository import Repository
from services.settings import *
from authentication.models import UserModel

class TestConnection(object):

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

class TestRepository(object):

    def setup(self):
        database = 'test_connection'
        self.connection = Connection(server=SERVER, database=database)
        self.repository = Repository(connection=self.connection)

    def teardown(self):
        if self.connection and self.connection.database :
            self.connection.server.delete(self.connection.database)

    def test_should_persist_and_load_document_to_database(self):
        document = DocumentBase(document_type='TestDocument')

        document = self.repository.save(document)
        assert document.document_type == 'TestDocument'

        document1 = self.repository.load(document.id)
        assert document1

    def test_should_persist_and_load_view_to_database(self):
        self.repository.create_view("test","by_test_entity","function(doc){emit(null,doc);}","")

        view = self.repository.load("_design/test")
        assert view
        assert view["views"]["by_test_entity"]

    def test_should_return_none_if_documentid_is_empty(self):
        repository = Repository(connection=self.connection)
        user = repository.load('',UserModel)
        assert not user
