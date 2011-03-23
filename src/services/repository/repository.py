from services.repository.DocumentBase import DocumentBase
from services.repository.connection import Connection

class Repository:

    def __init__(self, connection):
        self.connection = connection
        self.database = connection.database

    def save(self, document):
        document.store(self.database)
        return document

    def delete(self, document):
        self.database.delete(document)

    def load(self, id, document_class=DocumentBase):
        if id:
            return document_class.load(self.database, id)
        return None
