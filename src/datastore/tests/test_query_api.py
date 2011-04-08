import datetime
from datastore.database import get_db_manager, _delete_db_and_remove_db_manager
import unittest
from datastore import config
from datastore import views
from datastore.entity import Entity

class TestQueryApi(unittest.TestCase):

    def setUp(self):
        self.manager = get_db_manager('http://localhost:5984/', 'mangrove-test')

    def tearDown(self):
        _delete_db_and_remove_db_manager(self.manager)

    def create_reporter(self):
        r = Entity(self.manager, entity_type=["Reporter"])
        r.save()
        return r

    def test_can_create_views(self):
        views.create_views(self.manager)
        self.assertTrue(views.exists_view("by_location", self.manager))
        self.assertTrue(views.exists_view("by_time", self.manager))
        self.assertTrue(views.exists_view("by_values", self.manager))

    def test_should_get_current_values_for_entity(self):
        views.create_views(self.manager)
        e = Entity(self.manager, entity_type=["Health_Facility.Clinic"],location=['India','MH','Pune'])
        id = e.save()
        e.add_data(data = [("beds", 10), ("meds",  20), ("doctors", 2)], event_time=datetime.datetime(2011,01,01))
        e.add_data(data = [("beds", 15), ("doctors",2)], event_time=datetime.datetime(2011,02,01))
        e.add_data(data = [("beds", 20), ("meds", 05), ("doctors",2)], event_time=datetime.datetime(2011,03,01))

        # values asof
        data_fetched = e.values( { "beds" : "latest", "meds" : "latest", "doctors":"latest"},
                                 asof=datetime.datetime(2011,01,31))
        self.assertEqual(data_fetched["beds"], 10)
        self.assertEqual(data_fetched["meds"], 20)
        self.assertEqual(data_fetched["doctors"], 2)

        # values asof
        data_fetched = e.values( { "beds" : "latest", "meds" : "latest", "doctors":"latest"},
                                 asof=datetime.datetime(2011,03,2))
        self.assertEqual(data_fetched["beds"], 20)
        self.assertEqual(data_fetched["meds"], 5)
        self.assertEqual(data_fetched["doctors"], 2)

        # current values
        data_fetched = e.values( { "beds" : "latest", "meds" : "latest", "doctors":"latest"} )
        self.assertEqual(data_fetched["beds"], 20)
        self.assertEqual(data_fetched["meds"], 5)
        self.assertEqual(data_fetched["doctors"], 2)



