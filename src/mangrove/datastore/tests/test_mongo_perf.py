# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from datetime import datetime
import unittest
import pymongo
import datetime
from pymongo.code import Code


class TestMapReduce(unittest.TestCase):
    def setUp(self):
        self.db = pymongo.Connection().map_reduce_example
        self.NUM_ENTITIES = 800
        self.DATA_REC_PER_ENTITY = 12
        self.no_of_datarecord=self.NUM_ENTITIES*self.DATA_REC_PER_ENTITY

    def tearDown(self):
        self.db.output.drop()
        self.db.things.drop()

    def create_data_record(self, data, entity_type, entity_id, event_time):
        entity_doc = {'entity_type': entity_type, 'entity_id': entity_id, 'event_time': event_time, 'data': data}
        return self.db.things.insert(entity_doc)

    def test_map_reduce(self):
        data = [
                {"field_name": "beds", "value": 10}, {"field_name": "meds", "value": 12},
                {"field_name": "beds2", "value": 10}, {"field_name": "meds2", "value": 12},
                {"field_name": "beds3", "value": 10}, {"field_name": "meds3", "value": 12},
                {"field_name": "beds4", "value": 10}, {"field_name": "meds4", "value": 12},
                {"field_name": "beds5", "value": 10}, {"field_name": "meds5", "value": 12},
        ]
        for i in range(0,self.NUM_ENTITIES):
            for j in range(0,self.DATA_REC_PER_ENTITY):
                self.create_data_record(data=data,
                                entity_type="Clinic", entity_id='cl'+str(i),event_time=datetime.datetime.now())

        for i in range(0,self.no_of_datarecord):
            self.create_data_record(data=data,
                                entity_type="School", entity_id="cl01",
                                event_time=datetime.datetime.now())

        print "Firing Map Reduce..."
        start = datetime.datetime.now()
        reduce = Code("function (key, values) {"
                      "  var total = 0;"
                      "  print('test');"
                      "  for (var i = 0; i < values.length; i++) {"
                      "    total += values[i].count;"
                      "  }"
                      "  return {'count':total};"
                      "}")

        map = Code("function () {"
                   "  type=this.entity_type;"
                   "  id=this.entity_id;"
                   "  for(k in this.data){"
                   "  emit({'type':type,'id':id,'field_name':this.data[k].field_name}, {'count':this.data[k].value});"
                   "  };"
                   "}")

        result = self.db.things.map_reduce(map, reduce, "output", finalize=None,query={"entity_type": {"$all": ['Clinic']}})

        end = datetime.datetime.now()
        print "first time data.aggregate took %s" % (end - start,)
        self.assertTrue(False)