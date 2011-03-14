from datetime import  datetime
import couchdb
from nose.tools import *

from couchdb import Server

#Given a python data_record, store the same in couchdb as a json doc.
from paste.script.util.uuid import uuid1
from src.data_record.data_record import IntDataRecord2


class TestDataRecord:

    def setup(self):
        self.server = Server()
        try:
            DATA_STORE = 'data_store'
            self.db = self.server[DATA_STORE]
        except couchdb.http.ResourceNotFound:
            self.db = self.server.create(DATA_STORE)


    def test_save_new_data_record(self):
        assert_is_not_none(self.db)
        # E.g. REG PATIENT NAME Pat Age 10
        # PATID 1234 BP 128 PULSE 80
        d = self.create_data_record2("1",bp=129,pulse=80)
        d.store(self.db)
        saved_record = DataRecord.load(self.db,d.id)
        assert saved_record.id

    def test_fetch_latest_value_for_data_record2(self):
        self.create_data_record2("12",bp=123,pulse=45)
        self.create_data_record2("12",bp=143,pulse=78)
        self.create_data_record2("12",bp=193,pulse=95)
        latest_bp = self.fetch_latest_value_for2(id="12",field="bp")
        latest_pulse = self.fetch_latest_value_for2(id="12",field="pulse")
#        assert latest_bp == 193
#        assert latest_pulse == 95

    def test_create_int_data_record(self):
        self.create_data_record2("1",bp=123,pulse=45)

    def create_data_record2(self,entity_id,bp,pulse):
        d = IntDataRecord2()
        d.namespace = "org.global.ClinicRecord"
        now = datetime.now()
        d.created_at = now
        d.updated_at = now
        d.entity_uuid = entity_id
        d.field_name = "BP"
        d.value = bp
        e = IntDataRecord2()
        e.namespace = "org.global.ClinicRecord"
        now = datetime.now()
        e.created_at = now
        e.updated_at = now
        e.entity_uuid = entity_id
        e.field_name = "Pulse"
        e.value = pulse
        d.store(self.db)
        e.store(self.db)


    def fetch_latest_value_for(self, field):
        pass

    def fetch_latest_value_for2(self, id, field):
        return 0


