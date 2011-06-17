# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
import datetime
import unittest
from unittest.case import SkipTest
from datawinners.main.initial_couch_fixtures import create_data_dict
from mangrove.datastore.aggregrate import aggregate_by_form_code_python, Latest, Sum
from mangrove.datastore.data import EntityAggregration
from mangrove.datastore.database import  get_db_manager, _delete_db_and_remove_db_manager
from mangrove.datastore.datadict import DataDictType
from mangrove.datastore.documents import DataRecordDocument
from mangrove.datastore.entity import Entity, define_type
from mangrove.datastore import data
from mangrove.form_model.field import SelectField, IntegerField, TextField
from mangrove.form_model.form_model import FormModel
from mangrove.utils.dates import utcnow


class TestViewPerf(unittest.TestCase):
    def setUp(self):
        self.form_code = "Cl1"
        self.ENTITY_TYPE = ["Health_Facility", "Clinic"]
        self.dbm = get_db_manager(database='mangrove-test')
        self.meds_type = create_data_dict(dbm=self.dbm, name='Medicines', slug='meds', primitive_type='number',
                                          description='Number of medications')
        self.beds_type = create_data_dict(dbm=self.dbm, name='Beds', slug='beds', primitive_type='number',
                                          description='Number of beds')
        self.director_type = create_data_dict(dbm=self.dbm, name='Director', slug='dir', primitive_type='string',
                                              description='Name of director')
        self.patients_type = create_data_dict(dbm=self.dbm, name='Patients', slug='patients', primitive_type='number',
                                              description='Patient Count')
        self._create_form_model(self.form_code)
        self.create_clinic_type(self.ENTITY_TYPE)
        self.bulk=[]

    def tearDown(self):
        _delete_db_and_remove_db_manager(self.dbm)

    def _create_data_record_batch(self, DATA_REC_PER_ENTITY, e):
        for i in range(0, DATA_REC_PER_ENTITY):
            self.add_data_bulk(e, data=[("beds", 10, self.beds_type), ("meds", 10, self.meds_type),
                    ("beds1", 100, self.beds_type), ("meds1", 100, self.meds_type),
                    ("beds2", 1000, self.beds_type), ("meds2", 1000, self.meds_type),
                    ("beds3", 10000, self.beds_type), ("meds3", 10000, self.meds_type),
                    ("beds4", 100000, self.beds_type), ("meds4", 100000, self.meds_type),
            ])

    def _save_batch(self, BATCH):
        start = datetime.datetime.now()
        for s in range(0, len(self.bulk))[::BATCH]:
            start = datetime.datetime.now()
            r = self.dbm.database.update(self.bulk[s:s + BATCH])
        end = datetime.datetime.now()
        print "Bulk updates took %s" % (end - start,)

    def _create_entity_batch(self, NUM_ENTITIES):
        start = datetime.datetime.now()
        le = [Entity(self.dbm, entity_type=["Health_Facility", "Clinic"], location=['India', 'MH', 'Pune'])
              for x in range(0,
                             NUM_ENTITIES)]
        entity_docs = [x._doc for x in le]
        r = self.dbm.database.update(entity_docs)
        end = datetime.datetime.now()
        print "Updating entities took %s" % (end - start,)
        return le

    def test_should_create_with_bulk_upload(self):
        NUM_ENTITIES = 1000
        DATA_REC_PER_ENTITY = 52
        BATCH = (NUM_ENTITIES * DATA_REC_PER_ENTITY) / 4

        le = self._create_entity_batch(NUM_ENTITIES)

        print "data records"
        for e in le:
            self._create_data_record_batch(DATA_REC_PER_ENTITY, e)

        print "total bulk docs %s" % (len(self.bulk))
        print "bulk save !"

        self._save_batch(BATCH)

        print "Firing view..."
        start = datetime.datetime.now()
        values = data.aggregate(self.dbm, entity_type=["Health_Facility", "Clinic"],
                            aggregates={"beds": data.reduce_functions.LATEST,
                                        "meds": data.reduce_functions.SUM},aggregate_on=EntityAggregration()
                            )
        end = datetime.datetime.now()
        print "first time data.aggregate took %s" % (end - start,)

        start = datetime.datetime.now()

        values = aggregate_by_form_code_python(self.dbm, self.form_code,
                            aggregates={Latest("beds"),Sum("meds")},aggregate_on=EntityAggregration()
                            )
        end = datetime.datetime.now()
        print "first time aggregate_by_form_code_python took %s" % (end - start,)


        start = datetime.datetime.now()
#        values = data.aggregate(self.dbm, entity_type=["Health_Facility", "Clinic"],
#                            aggregates={"beds": data.reduce_functions.LATEST,
#                                        "meds": data.reduce_functions.SUM},aggregate_on=EntityAggregration()
#                            )
        values = data.aggregate(self.dbm, entity_type=["Health_Facility", "Clinic"],
                            aggregates={"beds": data.reduce_functions.LATEST,
                                        "meds": data.reduce_functions.SUM},aggregate_on=EntityAggregration()
                            )
        end = datetime.datetime.now()
        print "second time data.aggregate took %s" % (end - start,)

        start = datetime.datetime.now()

        values = aggregate_by_form_code_python(self.dbm, self.form_code,
                            aggregates={Latest("beds"),Sum("meds")},aggregate_on=EntityAggregration()
                            )
#        values = aggregate_by_form_code_python(self.dbm, self.form_code,
#                            aggregates={Latest("beds"),Sum("meds")},aggregate_on=EntityAggregration()
#                            )
        end = datetime.datetime.now()
        print "second time aggregate_by_form_code_python took %s" % (end - start,)

        print "Done!"


    def _create_form_model(self, form_code):
        self.default_ddtype = DataDictType(self.dbm, name='Default String Datadict Type', slug='string_default',
                                           primitive_type='string')
        self.default_ddtype.save()
        question1 = TextField(name="entity_question", code="ID", label="What is associated entity",
                              language="eng", entity_question_flag=True, ddtype=self.default_ddtype)
        question2 = TextField(name="question1_Name", code="Q1", label="What is your name",
                              defaultValue="some default value", language="eng",
                              ddtype=self.default_ddtype)
        question3 = IntegerField(name="Father's age", code="Q2", label="What is your Father's Age",
                                 ddtype=self.default_ddtype)
        question4 = SelectField(name="Color", code="Q3", label="What is your favourite color",
                                options=[("RED", 1), ("YELLOW", 2)], ddtype=self.default_ddtype)

        self.form_model = FormModel(self.dbm, entity_type=self.ENTITY_TYPE, name="aids", label="Aids form_model",
                                    form_code=form_code, type='survey', fields=[
                question1, question2, question3, question4])
        self.form_model__id = self.form_model.save()

    def create_clinic_type(self, entity_type):
        self.entity_type = entity_type
        define_type(self.dbm, entity_type)

    def add_data_bulk(self, e, data):
        data_record_doc = DataRecordDocument(
            entity_doc=e._doc,
            event_time=utcnow(),
            data=data,
            submission={'form_code':self.form_code}
            )
        self.bulk.append(data_record_doc)


