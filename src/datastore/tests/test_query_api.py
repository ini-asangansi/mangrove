import datetime
from databasemanager.database_manager import DatabaseManager
import datastore
from datastore.entity import Entity
from nose.tools import *
from datastore import config
from datastore.views import views

class TestQueryApi(object):

    def create_reporter(self):
        r = Entity("Reporter X", entity_type="Reporter")
        r.save()
        return r


    def test_can_create_views(self):
        views.create_views()
        manager = DatabaseManager(server=config._server, database=config._db)
        assert views.exists_view("by_location", manager)
        assert views.exists_view("by_time", manager)
        assert views.exists_view("by_values", manager)

    def test_should_get_current_values_for_entity(self):

        r = self.create_reporter()

        e = Entity("clinic X",entity_type="Health_Facility.Clinic",location=['India','MH','Pune'])
        id = e.save()
        e.submit_data_record({"beds" : 10,"meds" : 20, "doctors":2},reported_on=datetime.datetime(2011,01,01),reported_by=r)
        e.submit_data_record({"beds" : 15, "doctors":2},reported_on=datetime.datetime(2011,02,01),reported_by=r)
        e.submit_data_record({"beds" : 20,"meds" : 05, "doctors":2},reported_on=datetime.datetime(2011,03,01),reported_by=r)

        # values asof
        data_fetched = e.values( { "beds" : "latest", "meds" : "latest", "doctors":"latest"} ,asof=datetime.datetime(2011,01,31))
        assert_equal (data_fetched["beds"], 10)
        assert_equal (data_fetched["meds"], 20)
        assert_equal (data_fetched["doctors"], 2)

        # values asof
        data_fetched = e.values( { "beds" : "latest", "meds" : "latest", "doctors":"latest"} ,asof=datetime.datetime(2011,03,2))
        assert_equal (data_fetched["beds"], 20)
        assert_equal (data_fetched["meds"], 5)
        assert_equal (data_fetched["doctors"], 2)

        # current values
        data_fetched = e.values( { "beds" : "latest", "meds" : "latest", "doctors":"latest"} )
        assert_equal (data_fetched["beds"], 20)
        assert_equal (data_fetched["meds"], 5)
        assert_equal (data_fetched["doctors"], 2)



