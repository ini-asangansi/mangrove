from datetime import datetime
import couchdb
from couchdb.client import Server
from couchdb.design import ViewDefinition
from couchdb.mapping import Document, IntegerField, TextField, DateTimeField, Field, ListField, DictField, DictField, Mapping, Mapping
from nose.tools import *
from src.data_record.data_record import DataRecord2, IntDataRecord2, DateTimeDataRecord2, FloatDataRecord2

class TestHierarchyAggregate:
    DATA_STORE = "test_data_store"

    @classmethod
    def setup_class(klass):
        DATA_STORE = klass.DATA_STORE
        klass.server = Server()
        try:
            if klass.server[DATA_STORE]:
                klass.server.delete(DATA_STORE)
        except couchdb.http.ResourceNotFound:
            pass
        klass.db = klass.server.create(DATA_STORE)
        klass.create_views()

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
                                for(i in doc.attr){
                                    field_dict = doc.attr[i];
                                    if (field_dict.type == "Number"){
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

    @classmethod
    def teardown_class(klass):
        pass

    def setup(self):
        self.server = self.__class__.server
        self.db = self.server[self.__class__.DATA_STORE]

    def test_verify_total_num_beds_across_clinics(self):
        #create clinics
        a = self.create_clinic(1,"India.Maharashtra.Pune","Clinic 1")
        self.create_clinic_record(a,beds = 10,arv = 100,event_time = datetime(2011,01,01))

        a = self.create_clinic(2,"India.Karnataka.Bangalore","Clinic 2")
        self.create_clinic_record(a,beds = 100,arv = 200,event_time = datetime(2011,02,01))

        a = self.create_clinic(3,"India.Maharashtra.Mumbai","Clinic 3")
        self.create_clinic_record(a,beds = 50,arv = 150,event_time = datetime(2011,02,01))

        a = self.create_clinic(4,"India.Maharashtra.Pune","Clinic 4")
        self.create_clinic_record(a,beds = 250,arv = 50,event_time = datetime(2011,01,01))

        a = self.create_clinic(5,"India.Karnataka.Bangalore","Clinic 5")
        self.create_clinic_record(a,beds = 150,arv = 150,event_time = datetime(2011,01,01))

        a = self.create_clinic(6,"India.Maharashtra.Pune","Clinic 6")
        self.create_clinic_record(a,beds = 10,arv = 15,event_time = datetime(2011,01,01))

        beds = self.fetch_total_num_of_beds()
        assert beds == 570

    def test_aggregate_tw_employees(self):
        a = self.create_employee(1,"US.ChicagoState.Chicago")
        b = self.create_employee(2,"India.Karnataka.Bangalore")
        c = self.create_employee(3,"US.Washington.New_York")
        d = self.create_employee(4,"India.Maharashtra.Pune")
        e = self.create_employee(5,"India.Karnataka.Bangalore")
        f = self.create_employee(6,"UK.LondonState.London")
        self.create_emp_record(a,"Roy","Chicago",90000,datetime(2011,01,01))
        self.create_emp_record(b,"Rohit","Bangalore",5000,datetime(2011,01,11))
        self.create_emp_record(c,"Ola","New York",40000,datetime(2010,01,01))
        self.create_emp_record(d,"Chai","Pune",2000,datetime(2010,02,01))
        self.create_emp_record(e,"Sudhir","Bangalore",70000,datetime(2011,03,01))
        self.create_emp_record(f,"Jeff","London",10000,datetime(2011,03,01))

        total_india_count = self.fetch_emp_count("India")
        total_uk_count = self.fetch_emp_count("UK")
        total_us_count = self.fetch_emp_count("US")

        assert total_india_count == 3
        assert total_uk_count == 1
        assert total_us_count == 2

    def create_data_record(self, id, fieldname, value,event_time,namespace):
        if type(value) == type(1):
            d = IntDataRecord2()
        elif type(value) == type(1.0):
            d = FloatDataRecord2()
        elif isinstance(value,datetime):
            d = DateTimeDataRecord2()
        else:
            d = DataRecord2()
        d.namespace = namespace
        now = datetime.now()
        d.created_at = now
        d.updated_at = now
        d.entity_uuid = id
        d.field_name = fieldname
        d.value = value
        d.event_time = event_time
        d.store(self.db)

    def create_emp_record(self,emp,name,location,salary,event_time):
        self.create_data_record(emp.entity_id, "Name",name,event_time,"org.global.EmployeeRecord")
        self.create_data_record(emp.entity_id, "Location",location,event_time,"org.global.EmployeeRecord")
        self.create_data_record(emp.entity_id, "Salary",salary,event_time,"org.global.EmployeeRecord")
        if emp.attr:
            for a in emp.attr:
                if a["field"] == "Name":
                    a["value"] = name
                    a["type"] = "Text"
                    a["timestamp"] = event_time
                if a["field"] == "Location":
                    a["value"] = location
                    a["type"] = "Text"
                    a["timestamp"] = event_time
                if a["field"] == "Salary":
                    a["value"] = salary
                    a["type"] = "Number"
                    a["timestamp"] = event_time
        else:
            emp.attr.append(dict(field="Name",value=name,type = "Text",timestamp=event_time))
            emp.attr.append(dict(field="Location",value=location,type = "Text",timestamp=event_time))
            emp.attr.append(dict(field="Salary",value=salary,type = "Number",timestamp=event_time))
        emp.store(self.db)

    def fetch_emp_count(self, location):
        rows = self.db.view('by_location/by_location',group_level=3).rows
        for i in rows:
            if location in i.key:
                return i.value
        return 0

    def create_employee(self, id,loc):
        return self.create_entity(id,loc,"org.global.Employee")

    def create_clinic(self, id, loc, name):
        return self.create_entity(id,loc,"org.global.Clinic")

    def create_clinic_record(self, clinic, beds, arv, event_time):
        self.create_data_record(clinic.entity_id, "beds",beds,event_time,"org.global.ClinicRecord")
        self.create_data_record(clinic.entity_id, "arv",arv,event_time,"org.global.ClinicRecord")
        if clinic.attr:
            for a in clinic.attr:
                if a["field"] == "beds":
                    a["value"] = beds
                    a["type"] = "Number"
                    a["timestamp"] = event_time
                if a["field"] == "arv":
                    a["value"] = arv
                    a["type"] = "Number"
                    a["timestamp"] = event_time
        else:
            clinic.attr.append(dict(field="beds",value=beds,type = "Number",timestamp=event_time))
            clinic.attr.append(dict(field="arv",value=arv, type = "Number",timestamp=event_time))
        clinic.store(self.db)

    def create_entity(self,id,loc,namespace):
        e =  Entity(entity_id = id,location=loc.split('.'),namespace= namespace)
        e.store(self.db)
        return e

    def fetch_total_num_of_beds(self):
        rows = self.db.view('by_field/by_field',group=True).rows
        for i in rows:
            if i.key == 'beds':
                return i.value
        return 0


class Entity(Document):
    entity_id = IntegerField()
    type = TextField(default="Entity")
    namespace = TextField()
    created_at = DateTimeField()
    updated_at = DateTimeField()
    location = ListField(TextField())
    name = TextField()
    attr = ListField(DictField(
                Mapping.build(
                    timestamp = DateTimeField(),
                    field = TextField(),
                    value = Field(),
                    type = TextField()
                )
            ))
