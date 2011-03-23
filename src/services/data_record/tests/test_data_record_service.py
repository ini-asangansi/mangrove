from datetime import datetime, date
from uuid import uuid4
from services.data_record.data_record_service import DataRecordService
from services.data_record.models import DataRecord
from services.entity_management.models import Organization

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
        organization = Organization(id=uuid4().hex, name = 'Organization Name')
        time = datetime.now()
        data_record = DataRecord(entity = organization, age = 25, time =time)

        data_record = service.create_data_record(data_record)
        loaded_data_record = service.load_data_record(data_record.id)
        self.test_data_record_id = data_record.id
        assert loaded_data_record
        assert loaded_data_record.entity.entity_type == 'Organization'
        assert loaded_data_record.age == str(25)
        assert loaded_data_record.time == str(time)




        
