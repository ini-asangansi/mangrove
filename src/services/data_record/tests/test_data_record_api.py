from datetime import datetime
from couchdb.design import ViewDefinition
from services.repository.repository import RepositoryForTests
from services.repository.connection import Connection
from services.entity_management.entity_management_service import EntityManagementService
from services.entity_management.models import Entity
from uuid import uuid4
from services.data_record.data_record_service import DataRecordService
from services.data_record.models import DataRecord


class TestDataRecordApi:

    test_data_record_id = ''

    def setup(self):
        self.repository = RepositoryForTests(Connection())

    def teardown(self):
        self.repository.delete_database()

    def create_clinic(self,id,location,name):

        entity_service = EntityManagementService(self.repository)
        clinic= Entity(id=id,entity_type = 'clinic',name=name,location=location)
        clinic = entity_service.create_entity(clinic)
        return clinic


    def create_clinic_records(self):
        data_service = DataRecordService(self.repository)
        clinic = self.create_clinic(uuid4().hex, ["India","Maharashtra","Pune"], "Clinic 1")
        data_record = DataRecord(entity=clinic,beds = 10,arv = 100,event_time=datetime.now())
        data_service.create_data_record(data_record)
        clinic = self.create_clinic(uuid4().hex, ["India","Karnataka","Bangalore"], "Clinic 2")
        data_record = DataRecord(entity=clinic, beds=100, arv=200, event_time=datetime(2011, 02, 01))
        data_service.create_data_record(data_record)
        clinic = self.create_clinic(uuid4().hex, ["India","Maharashtra","Mumbai"], "Clinic 3")
        data_record = DataRecord(entity=clinic, beds=50, arv=150, event_time=datetime(2011, 02, 01))
        data_service.create_data_record(data_record)
        clinic = self.create_clinic(uuid4().hex, ["India","Maharashtra","Pune"], "Clinic 4")
        data_record=DataRecord(clinic, beds=250, arv=50, event_time=datetime(2011, 01, 01))
        data_service.create_data_record(data_record)
        clinic = self.create_clinic(uuid4().hex, ["India","Karnataka","Bangalore"], "Clinic 5")
        data_record = DataRecord(clinic, beds=150, arv=150, event_time=datetime(2011, 01, 01))
        data_service.create_data_record(data_record)
        clinic = self.create_clinic(uuid4().hex, ["India","Maharashtra","Pune"], "Clinic 6")
        data_record = DataRecord(clinic, beds=10, arv=15, event_time=datetime(2011, 01, 01))
        data_service.create_data_record(data_record)

    def test_total_num_beds_across_clinics(self):
        #create clinics
        self.create_clinic_records()
        beds = self.fetch_total_num_of_beds()
        assert beds == 570

    def fetch_total_num_of_beds(self):
        rows = self.repository.load_all_rows_in_view('clinic/by_location',group=True, group_level=1)
        for i in rows:
            if i.key == ['beds']:
                return i.value['sum']
        return 0
