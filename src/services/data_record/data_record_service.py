from services.data_record.models import DataRecord
from services.repository.connection import Connection
from services.repository.repository import Repository

class DataRecordService:

    def __init__(self, repository=Repository(Connection())):
        self.repository = repository

    def create_data_record(self, data_record):
        return self.repository.save(data_record)

    def load_data_record(self, data_record):
        return self.repository.load(data_record, DataRecord)

    