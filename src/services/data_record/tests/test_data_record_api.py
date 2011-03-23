from datetime import datetime
from couchdb.design import ViewDefinition
from services.repository.repository import Repository
from services.repository.connection import Connection
from services.entity_management.entity_management_service import EntityManagementService
from services.entity_management.models import Entity
from uuid import uuid4
from services.data_record.data_record_service import DataRecordService
from services.data_record.models import DataRecord

class TestDataRecordApi:

    test_data_record_id = ''

    def setup(self):
        self.repository = Repository(Connection())

#    def teardown(self):
#        document = self.repository.load(self.test_data_record_id)
#        self.repository.delete(document)

    def create_clinic(self,id,location,name):

        entity_service = EntityManagementService(self.repository)
        clinic= Entity(id=id,entity_type = 'clinic',name=name,location=location)
        entity_service.create_entity(clinic)
        return clinic


    def create_clinic_records(self):
        data_service = DataRecordService(self.repository)
        a = self.create_clinic("1", ["India","Maharashtra","Pune"], "Clinic 1")
        data_record = DataRecord(entity=a,beds = 10,arv = 100,event_time=datetime(2011, 01, 01))
        data_service.create_data_record(data_record)
        a = self.create_clinic("2", "India.Karnataka.Bangalore", "Clinic 2")
        data_record = DataRecord(entity=a, beds=100, arv=200, event_time=datetime(2011, 02, 01))
        data_service.create_data_record(data_record)
        a = self.create_clinic("3", "India.Maharashtra.Mumbai", "Clinic 3")
        data_record = DataRecord(entity=a, beds=50, arv=150, event_time=datetime(2011, 02, 01))
        data_service.create_data_record(data_record)
        a = self.create_clinic("4", "India.Maharashtra.Pune", "Clinic 4")
        data_record=DataRecord(a, beds=250, arv=50, event_time=datetime(2011, 01, 01))
        data_service.create_data_record(data_record)
        a = self.create_clinic("5", "India.Karnataka.Bangalore", "Clinic 5")
        data_record = DataRecord(a, beds=150, arv=150, event_time=datetime(2011, 01, 01))
        data_service.create_data_record(data_record)
        a = self.create_clinic("6", "India.Maharashtra.Pune", "Clinic 6")
        data_record = DataRecord(a, beds=10, arv=15, event_time=datetime(2011, 01, 01))
        data_service.create_data_record(data_record)

    @classmethod
    def create_views(klass):
        view = ViewDefinition('by_field','by_field','''
         function(doc){for(i in doc.attr){
            field_dict = doc.attr[i];
            if (field_dict.type == "Number")
                emit(field_dict.field,parseInt(field_dict.value));
         }}''','''_sum''')
        view.sync(klass.db)
        view = ViewDefinition('by_location','by_location','''function(doc) {
                                for(i in doc.attributes){
                                    field_dict = doc.attributes[i]
                                        key = [doc.namespace, field_dict.field];
                                        for (v in doc.location){
                                            key.push(doc.location[v]);
                                        }
                                    key.push(field_dict.timestamp);
                                    emit(key,parseInt(field_dict.value));
                                    }
                                }
                                }''','''_count'''
                              )
        view.sync(klass.db)

        view = ViewDefinition('by_location_time','by_location_time','''function(doc) {
                                    if ((doc.type == "Data_Record")&& (doc.field_type=="Number")){
                                        for (location in doc.location_path){
                                            key = [doc.namespace, doc.field_name];
                                            date = new Date(doc.event_time)
                                            var year = date.getFullYear();
                                            var month = date.getMonth()+1;
                                            key.push(location);
                                            key.push(doc.location_path[location]);
                                            key.push(year);
                                            key.push(month);
                                            emit(key,parseInt(doc.value));
                                        }
                                    }
                                    }''','''_sum'''
                              )
        view.sync(klass.db)

#    def test_total_num_beds_across_clinics(self):
#        #create clinics
#        self.create_clinic_records()
#        assert True
##        beds = self.fetch_total_num_of_beds()
##        assert beds == 570

    def fetch_total_num_of_beds(self):
        rows = self.repository.load_all_rows_in_view('by_field/by_field',group=True)
        for i in rows:
            if i.key == 'beds':
                return i.value
        return 0
        