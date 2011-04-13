import datetime
from datastore.database import get_db_manager, _delete_db_and_remove_db_manager
import unittest
from pytz import UTC
from datastore import views
from datastore.entity import Entity
from datastore import data

class TestQueryApi(unittest.TestCase):

    def setUp(self):
        self.manager = get_db_manager('http://localhost:5984/', 'mangrove-test')

    def tearDown(self):
        _delete_db_and_remove_db_manager(self.manager)
        pass

    def create_reporter(self):
        r = Entity(self.manager, entity_type=["Reporter"])
        r.save()
        return r

    def test_can_create_views(self):
        self.assertTrue(views.exists_view("by_location", self.manager))
        self.assertTrue(views.exists_view("by_time", self.manager))
        self.assertTrue(views.exists_view("by_values", self.manager))

    def test_should_get_current_values_for_entity(self):
        e = Entity(self.manager, entity_type=["Health_Facility.Clinic"],location=['India','MH','Pune'])
        id = e.save()
        e.add_data(data = [("beds", 10), ("meds",  20), ("doctors", 2)], event_time=datetime.datetime(2011,01,01, tzinfo = UTC))
        e.add_data(data = [("beds", 15), ("doctors",2)], event_time=datetime.datetime(2011,02,01, tzinfo = UTC))
        e.add_data(data = [("beds", 20), ("meds", 05), ("doctors",2)], event_time=datetime.datetime(2011,03,01, tzinfo = UTC))

        # values asof
        data_fetched = e.values( { "beds" : "latest", "meds" : "latest", "doctors":"latest"},
                                 asof=datetime.datetime(2011,01,31, tzinfo = UTC))
        self.assertEqual(data_fetched["beds"], 10)
        self.assertEqual(data_fetched["meds"], 20)
        self.assertEqual(data_fetched["doctors"], 2)

        # values asof
        data_fetched = e.values( { "beds" : "latest", "meds" : "latest", "doctors":"latest"},
                                 asof=datetime.datetime(2011,03,2, tzinfo = UTC))
        self.assertEqual(data_fetched["beds"], 20)
        self.assertEqual(data_fetched["meds"], 5)
        self.assertEqual(data_fetched["doctors"], 2)

        # current values
        data_fetched = e.values( { "beds" : "latest", "meds" : "latest", "doctors":"latest"} )
        self.assertEqual(data_fetched["beds"], 20)
        self.assertEqual(data_fetched["meds"], 5)
        self.assertEqual(data_fetched["doctors"], 2)

    #         Query API tests. Not implemented
    def test_should_fetch_aggregates_for_entity_type(self):
        # Aggregate across all instances of an entity type

        # Setup: Create clinic entities        
        ENTITY_TYPE = ["Health_Facility","Clinic"]
        e = Entity(self.manager, entity_type=ENTITY_TYPE,location=['India','MH','Pune'])
        id = e.save()
        e.add_data(data = [("beds", 300), ("meds",  20), ("doctors", 2)],
                   event_time=datetime.datetime(2011,01,01, tzinfo = UTC))

        e = Entity(self.manager, entity_type=ENTITY_TYPE,location=['India','Karnataka','Bangalore'])
        id = e.save()
        e.add_data(data = [("beds", 100), ("meds",  250), ("doctors", 10)],
                   event_time=datetime.datetime(2011,05,01, tzinfo = UTC))

        e = Entity(self.manager, entity_type=ENTITY_TYPE,location=['India','MH','Mumbai'])
        id = e.save()
        e.add_data(data = [("beds", 200), ("meds",  50), ("doctors", 5)],
                   event_time=datetime.datetime(2011,03,01, tzinfo = UTC))

        values = data.fetch(entity_type=ENTITY_TYPE,aggregates = { "beds" : "avg" , "meds" : "sum"  })
        # values: {  'India' : [ ("beds" ,"avg",100), ("meds" ,"sum",10000)  ]  }
        self.assertEqual(values, { "Health_Facility.Clinic" : [("beds" ,"avg",200), ("meds" ,"sum",320)  ] })

#    def test_should_fetch_aggregates_for_entity_type_for_hierarchy_path(self):
#        # Aggregate across all instances of an entity type in a given location..say India.
#        # values: {  'India' : [ ("beds" ,"avg",100), ("meds" ,"sum",10000)  ]  }
#        values = data.fetch(entity_type=['health facility', 'clinic'],aggregates = { "beds" : "avg" , "meds" : "sum"  },
#                            aggregate_on = { 'type' : 'location', 'value' : "India"} )
#
#        # Return aggregate for all entities at the same level in the hierarchy.
#        # E.g, below will return the average bed count and total medicine count per state, where state = level 2 in the hierarchy (Country, State, City)
#        # values : {  'Karnataka' : [ ("beds" ,"avg",100), ("meds" ,"sum",1000)  ], 'Maharashtra' : [ ("beds" ,"avg",10), ("meds" ,"sum",1000) ]  }
#
#        values = data.fetch(entity_type=['health facility', 'clinic'],aggregates = { "beds" : "avg" , "meds" : "sum"  },
#                            aggregate_on = { 'type' : 'location', 'level' : 2} )
#
#
#    def test_should_fetch_aggregates_for_entity_type_filtered_by_time(self):
#        values = data.fetch(entity_type=['health facility', 'clinic'],aggregates = { "beds" : "avg" , "meds" : "sum"  },
#                                aggregate_on = { 'type' : 'location', 'value' : "India"}, starttime = "01/01/2011",endtime = "01/12/2011" )
#
#
#    def test_should_fetch_by_range(self):
#        #   Total num of patients age bw 20 to 35.
#        #   Handle inclusive/exclusive ranges.
#        values = data.fetch(entity_type=['patient'],aggregates = { "*" : "count" },filter = { "age" : [20,35] })
#
#    def test_should_fetch_all_entities_for_a_criteria(self):
#        # Return all clinic entities with beds = 129
#        entity.get_entities(entity_type = ['clinic'], filter = {'beds' : 129})
