# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

#  This is an integration test.
# Send sms, parse and save.
import unittest
from  mangrove import initializer

from mangrove.datastore.database import get_db_manager, _delete_db_and_remove_db_manager
from mangrove.datastore.documents import SubmissionLogDocument, DataRecordDocument
from mangrove.datastore.entity import define_type, get_by_short_code, create_entity
from mangrove.errors.MangroveException import  DataObjectAlreadyExists, EntityTypeDoesNotExistsException
from mangrove.form_model.field import TextField, IntegerField, SelectField
from mangrove.form_model.form_model import FormModel, NAME_FIELD, MOBILE_NUMBER_FIELD
from mangrove.form_model.validation import NumericConstraint, TextConstraint
from mangrove.transport.player.player import SMSPlayer, Request
from mangrove.transport.submissions import SubmissionHandler,get_submissions_made_for_form
from mangrove.datastore.datadict import DataDictType


class TestShouldSaveSMSSubmission(unittest.TestCase):
    def setUp(self):
        self.dbm = get_db_manager(database='mangrove-test')
        initializer.run(self.dbm)
        define_type(self.dbm, ["dog"])
        self.entity_type = ["HealthFacility", "Clinic"]
        define_type(self.dbm, self.entity_type)
        self.name_type = DataDictType(self.dbm, name='Name', slug='name', primitive_type='string')
        self.telephone_number_type = DataDictType(self.dbm, name='telephone_number', slug='telephone_number',
                                                  primitive_type='string')
        self.entity_id_type = DataDictType(self.dbm, name='Entity Id Type', slug='entity_id', primitive_type='string')
        self.stock_type = DataDictType(self.dbm, name='Stock Type', slug='stock', primitive_type='integer')
        self.color_type = DataDictType(self.dbm, name='Color Type', slug='color', primitive_type='string')

        self.name_type.save()
        self.telephone_number_type.save()
        self.stock_type.save()
        self.color_type.save()

        self.entity = create_entity(self.dbm, entity_type=["HealthFacility", "Clinic"],
                                    location=["India", "Pune"], aggregation_paths=None, short_code="cli1",
                                    )

        self.data_record_id = self.entity.add_data(data=[("Name", "Ruby", self.name_type)], submission=dict(submission_id="1"))

        reporter = create_entity(self.dbm, entity_type=["Reporter"],
                                 location=["India", "Pune"], aggregation_paths=None, short_code="REP1",
                                 )

        reporter.add_data(data=[(MOBILE_NUMBER_FIELD, '1234', self.telephone_number_type),
                                (NAME_FIELD, "Test_reporter", self.name_type)], submission=dict(submission_id="2"))

        question1 = TextField(name="entity_question", code="EID", label="What is associated entity",
                              language="eng", entity_question_flag=True, ddtype=self.entity_id_type)
        question2 = TextField(name="Name", code="NAME", label="Clinic Name",
                              defaultValue="some default value", language="eng", length=TextConstraint(4, 15),
                              ddtype=self.name_type)
        question3 = IntegerField(name="Arv stock", code="ARV", label="ARV Stock",
                                 range=NumericConstraint(min=15, max=120), ddtype=self.stock_type)
        question4 = SelectField(name="Color", code="COL", label="Color",
                                options=[("RED", 1), ("YELLOW", 2)], ddtype=self.color_type)

        self.form_model = FormModel(self.dbm, entity_type=self.entity_type, name="aids", label="Aids form_model",
                                    form_code="clinic", type='survey', fields=[question1, question2, question3])
        self.form_model.add_field(question4)
        self.form_model__id = self.form_model.save()

        self.submission_handler = SubmissionHandler(self.dbm)
        self.sms_player = SMSPlayer(self.dbm,self.submission_handler)

    def tearDown(self):
        _delete_db_and_remove_db_manager(self.dbm)

    def test_should_save_submitted_sms(self):
        text = "clinic +EID %s +name CLINIC-MADA +ARV 50 +COL a" % self.entity.short_code
        

        response = self.sms_player.accept(Request("sms", text, "1234", "5678"))

        self.assertTrue(response.success)

        data_record_id = response.datarecord_id
        data_record = self.dbm._load_document(id=data_record_id, document_class=DataRecordDocument)
        self.assertEqual(self.name_type.slug, data_record.data["Name"]["type"]["slug"])
        self.assertEqual(self.stock_type.slug, data_record.data["Arv stock"]["type"]["slug"])
        self.assertEqual(self.color_type.slug, data_record.data["Color"]["type"]["slug"])
        self.assertEqual("clinic", data_record.submission['form_code'])
        data = self.entity.values({"Name": "latest", "Arv stock": "latest", "Color": "latest"})
        self.assertEquals(data["Arv stock"], 50)
        self.assertEquals(data["Name"], "CLINIC-MADA")
        submission_log = self.dbm._load_document(response.submission_id, SubmissionLogDocument)
        self.assertEquals(data_record_id, submission_log.data_record_id)


    def test_should_give_error_for_wrong_integer_value(self):
        text = "clinic +EID %s +ARV 150 " % self.entity.id
        response = self.sms_player.accept(Request("sms", text, "1234", "5678"))
        self.assertFalse(response.success)
        self.assertEqual(len(response.errors), 1)

    def test_should_give_error_for_wrong_text_value(self):
        text = "clinic +EID CID001 +NAME ABC"
        
        response = self.sms_player.accept(Request("sms", text, "1234", "5678"))
        self.assertFalse(response.success)
        self.assertEqual(len(response.errors), 1)

    def test_get_submissions_for_form(self):
        id=self.dbm._save_document(SubmissionLogDocument(channel="transport", source=1234,
                                                      destination=12345, form_code="abc",
                                                      values={'Q1': 'ans1', 'Q2': 'ans2'},
                                                      status=False, error_message="", data_record_id='2345678'))
        id1 = self.dbm._save_document(SubmissionLogDocument(channel="transport", source=1234,
                                                      destination=12345, form_code="abc",
                                                      values={'Q1': 'ans12', 'Q2': 'ans22'},
                                                      status=False, error_message="", data_record_id='1234567'))
        self.dbm._save_document(SubmissionLogDocument(channel="transport", source=1234,
                                                      destination=12345, form_code="def",
                                                      values={'defQ1': 'defans12', 'defQ2': 'defans22'},
                                                      status=False, error_message="", data_record_id='345678'))

        submission_list, ids = get_submissions_made_for_form(self.dbm, "abc")
        self.assertEquals(2, len(submission_list))
        self.assertEquals({'Q1': 'ans12', 'Q2': 'ans22'}, submission_list[0]['values'])
        self.assertEquals({'Q1': 'ans1', 'Q2': 'ans2'}, submission_list[1]['values'])
        self.assertEquals(2, len(ids))
        self.assertListEqual(['1234567', '2345678'], ids)

    def test_error_messages_are_being_logged_in_submissions(self):
        text = "clinic +EID %s +ARV 150 " % self.entity.id
        
        self.sms_player.accept(Request("sms", text, "1234", "5678"))
        submission_list, ids = get_submissions_made_for_form(self.dbm, "clinic")
        self.assertEquals(1, len(submission_list))
        self.assertEquals("Answer 150 for question ARV is greater than allowed.  ", submission_list[0]['error_message'])


    def test_should_register_new_entity(self):
        text = "reg +n buddy +T dog +G 80 80 +D its a dog! +M 123456"
        
        response = self.sms_player.accept(Request("sms", text, "1234", "5678"))
        self.assertTrue(response.success)
        self.assertIsNotNone(response.datarecord_id)
        expected_short_code = "dog1"
        self.assertEqual(response.short_code, expected_short_code)
        a = get_by_short_code(self.dbm, expected_short_code, ["dog"])
        self.assertEqual(a.short_code, expected_short_code)

        text = "reg +N buddy +S bud +T dog +L 80 80 +D its a dog! +M 45557"
        
        response = self.sms_player.accept(Request("sms", text, "1234", "5678"))
        self.assertTrue(response.success)
        self.assertIsNotNone(response.datarecord_id)
        self.assertEqual(response.short_code, "bud", ["dog"])
        a = get_by_short_code(self.dbm, "bud", ["dog"])
        self.assertEqual(a.short_code, "bud")

        text = "reg +N buddy2 +T dog +L 80 80 +D its another dog! +M 78541"
        
        response = self.sms_player.accept(Request("sms", text, "1234", "5678"))
        self.assertTrue(response.success)
        self.assertIsNotNone(response.datarecord_id)
        expected_short_code = "dog3"
        self.assertEqual(response.short_code, expected_short_code)
        b = get_by_short_code(self.dbm, expected_short_code, ["dog"])
        self.assertEqual(b.short_code, expected_short_code)

    def test_should_return_error_for_registration_having_invalid_geo_data(self):
        INVALID_LATITUDE = 380
        text = "reg +N buddy2 +T dog +G %s 80 +D its another dog! +M 78541" % (INVALID_LATITUDE,)
        
        response = self.sms_player.accept(Request("sms", text, "1234", "5678"))
        self.assertFalse(response.success)
        self.assertEqual({'g': '380 is an invalid latitude, must be between -90 and 90'}, response.errors)

        INVALID_LONGITUDE = -184
        text = "reg +N buddy2 +T dog +G 80 %s +D its another dog! +M 78541" % (INVALID_LONGITUDE,)
        
        response = self.sms_player.accept(Request("sms", text, "1234", "5678"))
        self.assertFalse(response.success)
        self.assertEqual({'g': '-184 is an invalid longitude, must be between -180 and 180'}, response.errors)

    def test_should_log_submission(self):
        request = Request(transport="sms", message="reg +N buddy +S DOG3 +T dog", source="1234", destination="5678")
        
        response = self.sms_player.accept(request)
        submission_log = self.dbm._load_document(response.submission_id, SubmissionLogDocument)
        self.assertIsInstance(submission_log, SubmissionLogDocument)
        self.assertEquals(request.transport, submission_log.channel)
        self.assertEquals(request.source, submission_log.source)
        self.assertEquals(request.destination, submission_log.destination)
        self.assertEquals(True, submission_log. status)
        self.assertEquals("reg", submission_log.form_code)
        self.assertEquals({'n': 'buddy', 's': 'DOG3', 't': 'dog'}, submission_log.values)
        self.assertEquals(request.destination, submission_log.destination)
        self.assertEquals(response.datarecord_id, submission_log.data_record_id)


    def test_should_throw_error_if_entity_with_same_short_code_exists(self):
        with self.assertRaises(DataObjectAlreadyExists):
            text = "reg +N buddy +S DOG3 +T dog +L 80 80 +D its a dog! +M 123456"
            
            self.sms_player.accept(Request("sms", text, "1234", "5678"))
            text = "reg +N buddy2 +S dog3 +T dog +L 80 80 +D its a dog! +M 123456"
            
            self.sms_player.accept(Request("sms", text, "1234", "5678"))

    def test_should_throw_error_if_entityType_doesnt_exist(self):
        with self.assertRaises(EntityTypeDoesNotExistsException):
            text = "reg +N buddy1 +S DOG3 +T cat +L 80 80 +D its another dog! +M 1234567"
            
            self.sms_player.accept(Request("sms", text, "1234", "5678"))

    def test_entity_instance_is_case_insensitive(self):
        text = "clinic +EID %s +name CLINIC-MADA +ARV 50 +COL a" % "CLI1"

        response = self.sms_player.accept(Request("sms", text, "1234", "5678"))

        self.assertTrue(response.success)

    def test_questionnaire_code_is_case_insensitive(self):
        text = "CLINIC +EID %s +name CLINIC-MADA +ARV 50 +COL a" % "cli1"

        response = self.sms_player.accept(Request("sms", text, "1234", "5678"))

        self.assertTrue(response.success)