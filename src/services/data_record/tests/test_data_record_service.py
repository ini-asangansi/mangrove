from uuid import uuid4
from services.data_record.data_record_service import DataRecordService
from services.data_record.models import DataRecord

from services.repository.connection import Connection
from services.repository.repository import Repository

class TestDataRecordService:

    test_data_record_id = ''
    
    def setup(self):
        self.repository = Repository(Connection())

    def teardown(self):
        document = self.repository.load(self.test_data_record_id)
        self.repository.delete(document)

    def test_should_create_data_record(self):
        service = DataRecordService(self.repository)
        data_record = DataRecord(id=uuid4().hex, name = 'Test Entity', age = 25)

        service.create_data_record(data_record)
        loaded_data_record = service.load_data_record(data_record.id)
        self.test_data_record_id = data_record.id

        assert loaded_data_record
        assert loaded_data_record.name == 'Test Entity'
        assert loaded_data_record.age == 25




        
