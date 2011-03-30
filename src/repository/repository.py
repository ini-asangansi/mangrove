from couchdb.design import ViewDefinition
from services.repository.DocumentBase import DocumentBase
from services.repository.connection import Connection

class Repository:

    def __init__(self, connection = Connection()):
        self.connection = connection
        self.database = connection.database

    def load_all_rows_in_view(self,view_name,**values):
        return self.database.view(view_name,**values).rows

    def create_view(self,view_name,map,reduce, view_document='mangrove_views'):
        view = ViewDefinition(view_document,view_name,map,reduce)
        view.sync(self.database)

    def save(self, document):
        document.store(self.database)
        return document

    def delete(self, document):
        self.database.delete(document)

    def load(self, id, document_class=DocumentBase):
        if id:
            return document_class.load(self.database, id)
        return None

class RepositoryForTests(Repository):
    def delete_database(self):
        self.connection.server.delete(self.database)
