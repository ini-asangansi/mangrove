# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from datetime import datetime, timedelta
from django.contrib.auth.models import User, Group
from mock import patch
from datawinners import initializer
from datawinners.main.utils import get_database_manager_for_user
from datawinners.project.models import Project
from datawinners.submission.views import SMS
from mangrove.datastore.datadict import create_datadict_type, get_datadict_type_by_slug
from mangrove.datastore.entity import  define_type, create_entity, get_by_short_code
from pytz import UTC
from mangrove.errors.MangroveException import EntityTypeAlreadyDefined, DataObjectNotFound, DataObjectAlreadyExists
from mangrove.form_model.field import TextField, IntegerField, DateField, SelectField, GeoCodeField
from mangrove.form_model.form_model import FormModel, NAME_FIELD, MOBILE_NUMBER_FIELD, DESCRIPTION_FIELD, get_form_model_by_code
from mangrove.form_model.validation import NumericConstraint, TextConstraint
from mangrove.transport.player.player import Request, SMSPlayer
from mangrove.transport.reporter import REPORTER_ENTITY_TYPE
from mangrove.transport.submissions import SubmissionHandler


class DateTimeMocker(object):

    def __init__(self):
        self.datetime_patcher = patch("mangrove.datastore.entity.utcnow")
        self.datetime_mock = self.datetime_patcher.start()

    def set_date_time_now(self,val):
        self.datetime_mock.return_value = val

    def end_mock(self):
        self.datetime_patcher.stop()


def create_or_update_entity(manager, entity_type, location, aggregation_paths, short_code, geometry=None):
    entity = None
    try:
        entity = create_entity(manager, entity_type, location, aggregation_paths, short_code, geometry)
    except DataObjectAlreadyExists as e:
        entity = get_by_short_code(manager, short_code, entity_type)
        entity.delete()
        entity = create_entity(manager, entity_type, location, aggregation_paths, short_code, geometry)
    finally:
        return entity

def define_entity_instance(manager, entity_type, location, short_code, geometry, name=None, mobile_number=None, description=None):
    e = create_or_update_entity(manager, entity_type=entity_type, location=location, aggregation_paths=None,
                         short_code=short_code, geometry=geometry)
    name_type = create_data_dict(manager, name='Name Type', slug='Name', primitive_type='string')
    mobile_type = create_data_dict(manager, name='Mobile Number Type', slug='mobile_number', primitive_type='string')
    description_type = create_data_dict(manager, name='Description', slug='description', primitive_type='string')
    e.add_data(data=[(NAME_FIELD,name,name_type)])
    e.add_data([(MOBILE_NUMBER_FIELD,mobile_number,mobile_type)])
    e.add_data([(DESCRIPTION_FIELD,description,description_type)])
    return e

def create_entity_types(manager, entity_types):
    for entity_type in entity_types:
        try:
            define_type(manager, entity_type)
        except EntityTypeAlreadyDefined:
            pass


def create_data_dict(dbm, name, slug, primitive_type, description=None):
    try:
        existing = get_datadict_type_by_slug(dbm, slug)
        existing.delete()
    except DataObjectNotFound:
        pass
    return create_datadict_type(dbm, name, slug, primitive_type, description)


def load_manager_for_default_test_account():
    DEFAULT_USER = "tester150411@gmail.com"
    user = User.objects.get(username=DEFAULT_USER)
    group = Group.objects.filter(name = "NGO Admins")
    user.groups.add(group[0])
    return get_database_manager_for_user(user)


def register(manager, entity_type, data, location, short_code):
    e = create_or_update_entity(manager, entity_type=entity_type, location=location, aggregation_paths=None,
                      short_code=short_code)
    e.add_data(data=data)
    return e

#Data Dict Types
def load_datadict_types(manager):
    meds_type = create_data_dict(dbm=manager, name='Medicines', slug='meds', primitive_type='number',
                                 description='Number of medications')
    beds_type = create_data_dict(dbm=manager, name='Beds', slug='beds', primitive_type='number',
                                 description='Number of beds')
    director_type = create_data_dict(dbm=manager, name='Director', slug='dir', primitive_type='string',
                                     description='Name of director')
    patients_type = create_data_dict(dbm=manager, name='Patients', slug='patients', primitive_type='geocode',
                                     description='Patient Count')


def load_clinic_entities(CLINIC_ENTITY_TYPE, manager):
    e = define_entity_instance(manager, CLINIC_ENTITY_TYPE, ['India', 'MP', 'Bhopal'], short_code="cid001",
                               geometry={"type": "Point", "coordinates": [23.2833, 77.35]},
                               name="Bhopal Clinic", description="This a clinic in Bhopal.", mobile_number="123456")
    e.set_aggregation_path("governance", ["Director", "Med_Officer", "Surgeon"])
    try:
        e.save()
    except Exception:
        pass
    e = define_entity_instance(manager, CLINIC_ENTITY_TYPE, ['India', 'MP', 'Satna'], short_code="cid002",
                               geometry={"type": "Point", "coordinates": [24.5667, 80.8333]},
                               name="Satna Clinic", description="This a clinic in Satna.", mobile_number="123457")
    e.set_aggregation_path("governance", ["Director", "Med_Supervisor", "Surgeon"])
    try:
        e.save()
    except Exception:
        pass
    e = define_entity_instance(manager, CLINIC_ENTITY_TYPE, ['India', 'MP', 'Jabalpur'], short_code="cid003",
                               geometry={"type": "Point", "coordinates": [23.2, 79.95]},
                               name="Jabalpur Clinic", description="This a clinic in Jabalpur.", mobile_number="123458")
    e.set_aggregation_path("governance", ["Director", "Med_Officer", "Doctor"])
    try:
        e.save()
    except Exception:
        pass
    e = define_entity_instance(manager, CLINIC_ENTITY_TYPE, ['India', 'MP', 'Khandwa'], short_code="cid004",
                               geometry={"type": "Point", "coordinates": [21.8333, 76.3667]},
                               name="Khandwa Clinic", description="This a clinic in Khandwa.", mobile_number="123459")
    e.set_aggregation_path("governance", ["Director", "Med_Supervisor", "Nurse"])
    try:
        e.save()
    except Exception:
        pass
    e = define_entity_instance(manager, CLINIC_ENTITY_TYPE, ['India', 'Kerala', 'Kochi'], short_code="cid005",
                               geometry={"type": "Point", "coordinates": [9.939248, 76.259625]},
                               name="Kochi Clinic", description="This a clinic in Kochi.", mobile_number="123460")
    e.set_aggregation_path("governance", ["Director", "Med_Officer", "Nurse"])
    try:
        e.save()
    except Exception:
        pass
    e = define_entity_instance(manager, CLINIC_ENTITY_TYPE, ['India', 'Madhya Pradesh', 'New Gwalior'],
                               short_code="cid006", geometry={"type": "Point", "coordinates": [26.227112, 78.18708]},
                               name="New Gwalior Clinic", description="This a clinic in New Gwalior.", mobile_number="1234561")
    e.set_aggregation_path("governance", ["Director", "Med_Officer", "Nurse"])
    try:
        e.save()
    except Exception:
        pass
    e = define_entity_instance(manager, CLINIC_ENTITY_TYPE, ['India', 'Madhya Pradesh', 'Indore'], short_code="cid007",
                               geometry={"type": "Point", "coordinates": [22.7167, 75.8]},
                               name="Indore Clinic", description="This a clinic in Indore.", mobile_number="1234562")
    e.set_aggregation_path("governance", ["Director", "Med_Officer", "Nurse"])
    try:
        e.save()
    except Exception:
        pass


def load_waterpoint_entities(WATER_POINT_ENTITY_TYPE, manager):
    e = define_entity_instance(manager, WATER_POINT_ENTITY_TYPE, ['India', 'Gujrat', 'Ahmedabad'], short_code="wp01",
                               geometry={"type": "Point", "coordinates": [23.0395677, 72.566005]},
                               name="Ahmedabad waterpoint", description="This a waterpoint in Ahmedabad.", mobile_number="1234563")
    e.set_aggregation_path("governance", ["Commune Head", "Commune Lead", "Commune People"])
    try:
        e.save()
    except Exception:
        pass
    e = define_entity_instance(manager, WATER_POINT_ENTITY_TYPE, ['India', 'Gujrat', 'Bhuj'], short_code="wp02",
                               geometry={"type": "Point", "coordinates": [23.251671, 69.66256]},
                               name="Bhuj waterpoint", description="This a waterpoint in Bhuj.", mobile_number="1234564")
    e.set_aggregation_path("governance", ["Commune Head", "Commune Lead", "Commune People"])
    try:
        e.save()
    except Exception:
        pass
    e = define_entity_instance(manager, WATER_POINT_ENTITY_TYPE, ['India', 'Haryana', 'Gurgaon'], short_code="wp03",
                               geometry={"type": "Point", "coordinates": [28.46385, 77.017838]},
                               name="Gurgaon waterpoint", description="This a waterpoint in Gurgaon.", mobile_number="1234564")
    e.set_aggregation_path("governance", ["Commune Head", "Commune Lead", "Commune People"])
    try:
        e.save()
    except Exception:
        pass


def create_clinic_projects(CLINIC_ENTITY_TYPE, manager):
    name_type = create_data_dict(manager, name='Name', slug='Name', primitive_type='string')
    # Entity id is a default type in the system.
    entity_id_type = get_datadict_type_by_slug(manager, slug='entity_id')
    age_type = create_data_dict(manager, name='Age Type', slug='age', primitive_type='integer')
    date_type = create_data_dict(manager, name='Report Date', slug='date', primitive_type='date')
    select_type = create_data_dict(manager, name='Choice Type', slug='choice', primitive_type='select')
    geo_code_type = create_data_dict(manager, name='GeoCode Type', slug='geo_code', primitive_type='geocode')
    question1 = TextField(label="entity_question", code="EID", name="What is associated entity?",
                          language="eng", entity_question_flag=True, ddtype=entity_id_type,
                          length=TextConstraint(min=1, max=12))
    question2 = TextField(label="Name", code="NA", name="What is your name?",
                          length=TextConstraint(min=1, max=10),
                          defaultValue="some default value", language="eng", ddtype=name_type)
    question3 = IntegerField(label="Father age", code="FA", name="What is age of father?",
                             range=NumericConstraint(min=18, max=100), ddtype=age_type)
    question4 = DateField(label="Report date", code="RD", name="What is reporting date?",
                          date_format="dd.mm.yyyy", ddtype=date_type)
    question5 = SelectField(label="Blood Group", code="BG", name="What is your blood group?",
                            options=[("O+", "a"), ("O-", "b"), ("AB", "c"), ("B+", "d")], single_select_flag=True,
                            ddtype=select_type)
    question6 = SelectField(label="Symptoms", code="SY", name="What are symptoms?",
                            options=[("Rapid weight loss", "a"), ("Dry cough", "b"), ("Pneumonia", "c"),
                                     ("Memory loss", "d"), ("Neurological disorders ", "e")], single_select_flag=False,
                            ddtype=select_type)
    question7 = GeoCodeField(name="What is the GPS code for clinic", code="GPS", label="What is the GPS code for clinic?",
                             language="eng", ddtype=geo_code_type)
    form_model = FormModel(manager, name="AIDS", label="Aids form_model",
                           form_code="cli001", type='survey',
                           fields=[question1, question2, question3, question4, question5, question6, question7],
                           entity_type=CLINIC_ENTITY_TYPE
    )
    try:
        qid = form_model.save()
    except DataObjectAlreadyExists as e:
        get_form_model_by_code(manager, "cli001").delete()
        qid = form_model.save()
    project = Project(name="Clinic Test Project", goals="This project is for automation", project_type="survey",
                      entity_type=CLINIC_ENTITY_TYPE[-1], devices=["sms"], activity_report='no')
    project.qid = qid
    try:
        project.save(manager)
    except Exception:
        pass
    form_model2 = FormModel(manager, name="AIDS", label="Aids form_model",
                            form_code="cli002", type='survey',
                            fields=[question1, question2, question3, question4, question5, question6, question7],
                            entity_type=CLINIC_ENTITY_TYPE)
    try:
        qid2 = form_model2.save()
    except DataObjectAlreadyExists as e:
        get_form_model_by_code(manager, "cli002").delete()
        qid2 = form_model2.save()
    project2 = Project(name="Clinic2 Test Project", goals="This project is for automation", project_type="survey",
                       entity_type=CLINIC_ENTITY_TYPE[-1], devices=["sms", "web"], activity_report='no')
    project2.qid = qid2
    try:
        project2.save(manager)
    except Exception:
        pass


def load_sms_data_for_cli001(manager):
    FEB = datetime(2011, 02, 28, hour=12, minute=00, second=00, tzinfo=UTC)
    MARCH = datetime(2011, 03, 01, tzinfo=UTC)
    DEC_2010 = datetime(2010, 12, 28, hour=00, minute=00, second=59, tzinfo=UTC)
    NOV_2010 = datetime(2010, 11, 26, hour=23, minute=59, second=59, tzinfo=UTC)
    today = datetime.today()
    THIS_MONTH = datetime(today.year,today.month,5,12,45,58)
    PREV_MONTH = THIS_MONTH - timedelta(days=8)
    sms_player = SMSPlayer(manager, SubmissionHandler(manager))
    FROM_NUMBER = '1234567890'
    TO_NUMBER = '261333782943'
    message1 = "reg +t  clinic +n  Clinic in Analalava  +l  Analalava  +g  -14.6333  47.7667  +d This is a Clinic in Analalava +m 987654321"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "reg +t  clinic +n  Clinic in Andapa  +l  Andapa  +g  -14.65  49.6167  +d This is a Clinic in Andapa  +m 87654322"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "reg +t  clinic +n  Clinic in Antalaha  +l  Antalaha  +g  -14.8833  50.25  +d This is a Clinic in Antalaha  +m 87654323"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "reg +t  clinic +n  Clinic in Antananarivo  +l  Antananarivo  +g  -18.8  47.4833  +d This is a Clinic in Antananarivo  +m 87654324"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "reg +t  clinic +n  Clinic in Diégo–Suarez +l  Diégo–Suarez +g  -12.35  49.3  +d This is a Clinic in Diégo–Suarez +m 87654325"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "reg +t  clinic +n  Clinic in Antsirabe  +l  Antsirabe  +g  -19.8167  47.0667  +d This is a Clinic in Antsirabe  +m 87654326"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "reg +t  clinic +n  Clinic in Besalampy  +l  Besalampy  +g  -16.75  44.5  +d This is a Clinic in Besalampy  +m 87654327"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "reg +t  clinic +n  clinique à Farafangana  +l  Farafangana  +g  -22.8  47.8333  +d This is a Clinic in Farafangana  +m 87654328"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "reg +t  clinic +n  Clinic in Fianarantsoa  +l  Fianarantsoa  +g  -21.45  47.1 +d  C'est une clinique à Fianarantsoa +m 87654329"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "reg +t  clinic +n  Clinic in Île Sainte–Marie  +l  Île Sainte–Marie  +g  -17.0833  49.8167  +d This is a Clinic in Île Sainte–Marie  +m 87654330"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "reg +t  clinic +n  Clinic in Mahajanga +l  Mahajanga +g  -15.6667  46.35  +d This is a Clinic in Mahajanga +m 87654331"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "reg +t  clinic +n  Clinic in Solapur  +l  Solapur  +g  17.6667 75.9  +d This is a Clinic in Solapur  +m 87654377"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "reg +t  clinic +n Clinic in Bangalore  +l  Bangalore  +g  12.9833 77.5833  +d This is a Clinic in Bangalore  +m 87654378"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "reg +t  clinic +n  Clinic in Belgaum  +l  Belgaum  +g  15.85 74.6167  +d This is a Clinic in Belgaum  +m 87654379"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "reg +t  clinic +n  Clinic in Bellary  +l  Bellary  +g  15.15 76.85  +d This is a Clinic in Bellary  +m 87654380"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "reg +t  clinic +n  Clinic in Hubli–Dharwad  +l  Hubli–Dharwad  +g  15.35 75.1667  +d This is a Clinic in Hubli–Dharwad  +m 87654381"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "reg +t  clinic +n  Clinic in Mandya  +l  Mandya  +g  12.55 76.9  +d This is a Clinic in Mandya  +m 87654382"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "reg +t  clinic +n  Clinic in Mangalore  +l  Mangalore  +g  12.9167 74.8833  +d This is a Clinic in Mangalore  +m 87654383"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "reg +t  clinic +n  Clinic in Mysore  +l  Mysore  +g  12.3 76.65  +d This is a Clinic in Mysore  +m 87654384"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    datetime_mocker = DateTimeMocker()
    datetime_mocker.set_date_time_now(FEB)
    # Total number of identical records = 3
    message1 = "cli001 +EID cid001 +NA Mr. Tessy +FA 58 +RD 28.02.2011 +BG c +SY ade +GPS 79.2 20.34567"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "cli001 +EID cid002 +NA Mr. Adam +FA 62 +RD 15.02.2011 +BG a +SY ab +GPS 74.2678 23.3567"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "cli001 +EID cid003 +NA Ms. Beth +FA 75 +RD 09.02.2011 +BG b +SY bc +GPS 18.245 29.3123"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))

    datetime_mocker.set_date_time_now(MARCH)
    # Total number of identical records = 4
    message1 = "cli001 +EID cid004 +NA Jannita +FA 90 +RD 07.03.2011 +BG b +SY bbe +GPS 45.233 28.3324"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "cli001 +EID cid005 +NA Aanda +RD 12.03.2011 +BG c +SY bd +GPS 40.2 69.3123"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = 'cli001 +EID cid006 +NA Ianda (",) +FA 34 +RD 27.03.2011 +BG d +SY be +GPS 38.3452 15.3345'
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "cli001 +EID cli26 +NA ànita +FA 45 +RD 07.03.2011 +BG b +SY bbe +GPS 45.233 28.3324"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "cli001 +EID cid004 +NA Amanda +RD 12.03.2011 +BG c +SY bd +GPS 40.2 69.3123"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = 'cli001 +EID cid005 +NA Vanda (",) +FA 34 +RD 27.03.2011 +BG d +SY be +GPS 38.3452 15.3345'
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "cli001 +EID cid006 +NA ànnita +FA 80 +RD 07.03.2011 +BG b +SY bbe +GPS 45.233 28.3324"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "cli001 +EID cli26 +NA Amanda +RD 12.03.2011 +BG c +SY bd +GPS 40.2 69.3123"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = 'cli001 +EID cid004 +NA Panda (",) +FA 34 +RD 27.03.2011 +BG d +SY be +GPS 38.3452 15.3345'
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "cli001 +EID cid005 +NA ànnita +FA 50 +RD 07.03.2011 +BG b +SY bbe +GPS 45.233 28.3324"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "cli001 +EID cid006 +NA Jimanda +RD 12.03.2011 +BG c +SY bd +GPS 40.2 69.3123"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = 'cli001 +EID cli26 +NA Kanda (",) +FA 64 +RD 27.03.2011 +BG d +SY be +GPS 38.3452 15.3345'
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "cli001 +EID cid004 +NA ànnita +FA 30 +RD 07.03.2011 +BG b +SY bbe +GPS 45.233 28.3324"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "cli001 +EID cid005 +NA Qamanda +RD 12.03.2011 +BG c +SY bd +GPS 40.2 69.3123"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = 'cli001 +EID cid006 +NA Huanda (*_*) +FA 74 +RD 27.03.2011 +BG d +SY be +GPS 38.3452 15.3345'
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))

    datetime_mocker.set_date_time_now(DEC_2010)
    # Total number of identical records = 4
    message1 = "cli001 +EID cli25 +FA 47 +RD 15.12.2010 +BG d +SY ace +GPS -58.3452 19.3345"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "cli001 +EID cli23 +NA De'melo +FA 38 +RD 27.12.2010 +BG c +SY ba +GPS 81.672 92.33456"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "cli001 +EID cli24 +NA Dono`mova +FA 24 +RD 06.12.2010 +BG b +SY cd +GPS 65.23452 -28.3456"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "cli001 +EID cli22 +NA Aàntra +FA 89 +RD 11.12.2010 +BG a +SY bd +GPS 45.234 89.32345"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))

    datetime_mocker.set_date_time_now(NOV_2010)
    # Total number of identical records = 3
    message1 = "cli001 +EID cli21 +NA ànnita +FA 90 +RD 07.11.2010 +BG b +SY bbe +GPS 45.233 28.3324"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "cli001 +EID cli20 +NA Amanda +RD 12.11.2010 +BG c +SY bd +GPS 40.2 69.3123"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = 'cli001 +EID cli8 +NA Kanda (",) +FA 34 +RD 27.11.2010 +BG d +SY be +GPS 38.3452 15.3345'
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "cli001 +EID cli21 +NA ànnita +FA 90 +RD 17.11.2010 +BG b +SY bbe +GPS 45.233 28.3324"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "cli001 +EID cli20 +NA Amanda +RD 12.11.2010 +BG c +SY bd +GPS 40.2 69.3123"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = 'cli001 +EID cli8 +NA Kanda (",) +FA 34 +RD 27.11.2010 +BG d +SY be +GPS 38.3452 15.3345'
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))

    datetime_mocker.set_date_time_now(PREV_MONTH)
    # Total number of identical records = 4
    message1 = "cli001 +EID cli9 +NA Demelo +FA 38 +RD 17.05.2011 +BG c +SY ba +GPS 19.672 92.33456"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "cli001 +EID cli10 +NA Zorro +FA 48 +RD 05.05.2011 +BG b +SY cd +GPS 23.23452 -28.3456"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "cli001 +EID cli11 +NA Aàntra +FA 98 +RD 12.05.2011 +BG a +GPS -45.234 89.32345"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "cli001 +EID cli12 +NA ànnita +FA 37 +RD 05.05.2011 +BG d +SY cbe +GPS -78.233 -28.3324"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "cli001 +EID cli9 +NA Demelo +FA 38 +RD 17.05.2011 +BG c +SY ba +GPS 19.672 92.33456"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "cli001 +EID cli10 +NA Zorro +FA 48 +RD 02.05.2011 +BG b +SY cd +GPS 23.23452 -28.3456"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "cli001 +EID cli11 +NA Aàntra +FA 95 +RD 12.05.2011 +BG a +GPS -45.234 89.32345"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "cli001 +EID cli12 +NA ànnita +FA 35 +RD 09.05.2010 +BG d +SY cbe +GPS -78.233 -28.3324"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "cli001 +EID cli9 +NA Demelo +FA 32 +RD 27.05.2011 +BG c +SY ba +GPS 19.672 92.33456"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "cli001 +EID cli10 +NA Zorro +FA 43 +RD 05.05.2011 +BG b +SY cd +GPS 23.23452 -28.3456"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "cli001 +EID cli11 +NA Aàntra +FA 91 +RD 12.05.2011 +BG a +GPS -45.234 89.32345"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "cli001 +EID cli12 +NA ànnita +FA 45 +RD 15.05.2010 +BG d +SY cbe +GPS -78.233 -28.3324"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))

    datetime_mocker.set_date_time_now(THIS_MONTH)
    # Total number of identical records = 4
    message1 = "cli001 +EID cli13 +NA Dmanda +FA 69 +RD 05.06.2011 +BG c +SY ce +GPS 40.2 69.3123"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "cli001 +EID cli14 +NA Vamand +FA 36 +RD 03.06.2011 +BG a +SY ace +GPS 58.3452 115.3345"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "cli001 +EID cli15 +NA M!lo +FA 88 +RD 02.06.2011 +SY ba +GPS 19.672 92.33456"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "cli001 +EID cli16 +NA K!llo +FA 88 +GPS 19.672 92.33456"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "cli001 +EID cli13 +NA Dmanda +FA 89 +RD 04.06.2011 +BG c +SY ce +GPS 40.2 69.3123"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "cli001 +EID cli14 +NA Vamand +FA 56 +RD 01.06.2011 +BG a +SY ace +GPS 58.3452 115.3345"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "cli001 +EID cli15 +NA M!lo +FA 45 +RD 07.06.2011 +SY ba +GPS 19.672 92.33456"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "cli001 +EID cli16 +NA K!llo +FA 28 +GPS 19.672 92.33456"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))

    datetime_mocker.end_mock()

    # Total number of identical records = 3
    message1 = "cli001 +EID cli17 +NA Catty +FA 78 +RD 15.06.2011 +BG b +SY dce +GPS 33.23452 -68.3456"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "cli001 +EID cli18 +NA àntra +FA 28 +RD 12.06.2011 +BG a +SY adb +GPS -45.234 169.32345"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "cli001 +EID cli19 +NA Tinnita +FA 37 +BG d +SY ace +GPS -78.233 -28.3324"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))

    message1 = "cli001 +EID cli17 +NA Catty +FA 98 +RD 25.06.2011 +BG b +SY dce +GPS 33.23452 -68.3456"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "cli001 +EID cli18 +NA àntra +FA 58 +RD 22.06.2011 +BG a +SY adb +GPS -45.234 169.32345"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))
    message1 = "cli001 +EID cli19 +NA Tinnita +FA 27 +BG d +SY ace +GPS -78.233 -28.3324"
    response = sms_player.accept(Request(transport=SMS, message=message1, source=FROM_NUMBER, destination=TO_NUMBER))


def load_data():
    manager = load_manager_for_default_test_account()
    initializer.run(manager)
    CLINIC_ENTITY_TYPE = ["clinic"]
    WATER_POINT_ENTITY_TYPE = ["waterpoint"]
    create_entity_types(manager, [CLINIC_ENTITY_TYPE, WATER_POINT_ENTITY_TYPE])
    load_datadict_types(manager)
    load_clinic_entities(CLINIC_ENTITY_TYPE, manager)
    load_waterpoint_entities(WATER_POINT_ENTITY_TYPE, manager)
    create_clinic_projects(CLINIC_ENTITY_TYPE, manager)
    #Register Reporter
    phone_number_type = create_data_dict(manager, name='Telephone Number', slug='telephone_number',
                                         primitive_type='string')
    first_name_type = create_data_dict(manager, name='First Name', slug='first_name', primitive_type='string')
    register(manager, entity_type=REPORTER_ENTITY_TYPE, data=[(MOBILE_NUMBER_FIELD, "1234567890", phone_number_type),
                                                              (NAME_FIELD, "Shweta", first_name_type)], location=[u'Madagascar', u'Toliary', u'Menabe', u'Mahabo', u'Beronono'],
             short_code="rep1")
    register(manager, entity_type=REPORTER_ENTITY_TYPE, data=[(MOBILE_NUMBER_FIELD, "261332592634", phone_number_type),
                                                              (NAME_FIELD, "David", first_name_type)], location=[u'Madagascar', u'Fianarantsoa', u'Haute matsiatra', u'Ambohimahasoa', u'Camp Robin'],
             short_code="rep2")
    load_sms_data_for_cli001(manager)
