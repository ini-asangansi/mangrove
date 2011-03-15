from datetime import datetime
import couchdb
from couchdb.client import Server
from couchdb.design import ViewDefinition
from couchdb.mapping import Document, IntegerField, TextField, DateTimeField, Field, ListField, DictField, DictField, Mapping, Mapping
from nose.tools import *
from src.data_record.data_record import DataRecord2, IntDataRecord2, DateTimeDataRecord2, FloatDataRecord2

class TestHierarchyAggregate:
    def setup(self):
        self.server = Server()
        try:
            DATA_STORE = 'data_store3'
            self.db = self.server[DATA_STORE]
        except couchdb.http.ResourceNotFound:
            self.db = self.server.create(DATA_STORE)
            self.create_views()

    def create_views(self):
        view = ViewDefinition('by_field','by_field','''
         function(doc){for(i in doc.attr){
            field_dict = doc.attr[i];
            if (field_dict.type == "Number")
                emit(field_dict.field,parseInt(field_dict.value));
         }}''','''_sum''')
        view.sync(self.db)


    def test_check_averages_across_entities(self):
#         create clinics
        a = self.create_clinic(1,"Pune","Clinic 1")
        self.create_clinic_record(a,beds = 10,arv = 100,event_time = datetime(2011,01,01))

        a = self.create_clinic(2,"Bangalore","Clinic 2")
        self.create_clinic_record(a,beds = 100,arv = 200,event_time = datetime(2011,02,01))

        a = self.create_clinic(3,"Mumbai","Clinic 3")
        self.create_clinic_record(a,beds = 50,arv = 150,event_time = datetime(2011,02,01))

        a = self.create_clinic(4,"Pune","Clinic 4")
        self.create_clinic_record(a,beds = 250,arv = 50,event_time = datetime(2011,01,01))

        a = self.create_clinic(5,"Bangalore","Clinic 5")
        self.create_clinic_record(a,beds = 150,arv = 150,event_time = datetime(2011,01,01))

        a = self.create_clinic(6,"Pune","Clinic 6")
        self.create_clinic_record(a,beds = 10,arv = 15,event_time = datetime(2011,01,01))

        beds = self.fetch_total_num_of_beds()
        assert beds == 570
#         create employess

#         check the average salary
#        check the average number of beds.

    
#
#    def test_aggregate_tw_employees(self):
#        a = self.create_employee(1,"Chicago")
#        b = self.create_employee(2,"Bangalore")
#        c = self.create_employee(3,"New York")
#        d = self.create_employee(4,"Pune")
#        e = self.create_employee(5,"Bangalore")
#        f = self.create_employee(6,"London")
#        self.create_emp_record(a,"Roy","Chicago",90000,datetime(2011,01,01))
#        self.create_emp_record(b,"Rohit","Bangalore",5000,datetime(2011,01,11))
#        self.create_emp_record(c,"Ola","New York",40000,datetime(2010,01,01))
#        self.create_emp_record(d,"Chai","Pune",2000,datetime(2010,02,01))
#        self.create_emp_record(e,"Sudhir","Bangalore",70000,datetime(2011,03,01))
#        self.create_emp_record(f,"Jeff","London",10000,datetime(2011,03,01))
#
#        total_india_count = self.fetch_emp_count("India")
#        total_uk_count = self.fetch_emp_count("UK")
#        total_us_count = self.fetch_emp_count("US")
#
#        assert total_india_count == 3
#        assert total_uk_count == 1
#        assert total_us_count == 2

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
                if a["field"] == "Location":
                    a["value"] = location
                    a["type"] = "Text"
                if a["field"] == "Salary":
                    a["value"] = salary
                    a["type"] = "Number"
        else:
            emp.attr.append(dict(field="Name",value=name,type = "Text"))
            emp.attr.append(dict(field="Location",value=location,type = "Text"))
            emp.attr.append(dict(field="Salary",value=salary,type = "Number"))
        emp.store(self.db)

    def fetch_emp_count(self, location):
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
                if a["field"] == "arv":
                    a["value"] = arv
                    a["type"] = "Number"
        else:
            clinic.attr.append(dict(field="beds",value=beds,type = "Number"))
            clinic.attr.append(dict(field="arv",value=arv, type = "Number"))
        clinic.store(self.db)

    def create_entity(self,id,loc,namespace):
        e =  Entity(entity_id = id,location=loc,namespace= namespace)
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
    location = TextField()
    name = TextField()
    attr = ListField(DictField(
                Mapping.build(
                    timestamp = DateTimeField(),
                    field = TextField(),
                    value = Field(),
                    type = TextField()
                )
            ))
