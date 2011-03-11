from datetime import datetime
import couchdb
from couchdb.client import Server
from couchdb.mapping import Document, IntegerField, TextField, DateTimeField, Field, ListField, DictField, DictField, Mapping, Mapping
from nose.tools import *
from src.data_record.data_record import DataRecord2

class TestHierarchyAggregate:
    def setup(self):
        self.server = Server()
        try:
            DATA_STORE = 'data_store'
            self.db = self.server[DATA_STORE]
        except couchdb.http.ResourceNotFound:
            self.db = self.server.create(DATA_STORE)
    
    def test_create_hierarchy(self):
        pass

    def test_aggregate_tw_employees(self):
        a = self.create_employee(1,"Chicago")
        b = self.create_employee(2,"Bangalore")
        c = self.create_employee(3,"New York")
        d = self.create_employee(4,"Pune")
        e = self.create_employee(5,"Bangalore")
        f = self.create_employee(6,"London")
        self.create_emp_record(a,"Roy","Chicago",90000)
        self.create_emp_record(b,"Rohit","Bangalore",5000)
        self.create_emp_record(c,"Ola","New York",40000)
        self.create_emp_record(d,"Chai","Pune",2000)
        self.create_emp_record(e,"Sudhir","Bangalore",70000)
        self.create_emp_record(f,"Jeff","London",10000)

        total_india_count = self.fetch_emp_count("India")
        total_uk_count = self.fetch_emp_count("UK")
        total_us_count = self.fetch_emp_count("US")

        assert total_india_count == 3
        assert total_uk_count == 1
        assert total_us_count == 2

    def create_data_record(self, emp_id, fieldname, value):
        d = DataRecord2()
        d.namespace = "org.global.EmployeeRecord"
        now = datetime.now()
        d.created_at = now
        d.updated_at = now
        d.entity_uuid = emp_id
        d.field_name = fieldname
        d.value = value
        d.store(self.db)

    def create_emp_record(self,emp,name,location,salary):
        self.create_data_record(emp.entity_id, "Name",name)
        self.create_data_record(emp.entity_id, "Location",location)
        self.create_data_record(emp.entity_id, "Salary",salary)
        if emp.attr:
            for a in emp.attr:
                if a["field"] == "Name":
                    a["value"] = name
                if a["field"] == "Location":
                    a["value"] = location
                if a["field"] == "Salary":
                    a["value"] = salary
        else:
            emp.attr.append(dict(field="Name",value=name))
            emp.attr.append(dict(field="Location",value=location))
            emp.attr.append(dict(field="Salary",value=salary))
        emp.store(self.db)

    def fetch_emp_count(self, location):
        return 0

    def create_employee(self, id,loc):
        e =  Entity(entity_id = id,location=loc,namespace= "org.global.Employee")
        e.store(self.db)
        return e

class Entity(Document):
    entity_id = IntegerField()
    type = TextField(default="Entity")
    namespace = TextField()
    created_at = DateTimeField()
    updated_at = DateTimeField()
    location = TextField()
    attr = ListField(DictField(
                Mapping.build(
                    timestamp = DateTimeField(),
                    field = TextField(),
                    value = Field(),
                )
            ))
