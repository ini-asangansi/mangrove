from datetime import datetime, date, time
from decimal import Decimal
import json
from couchdb.mapping import Field

# This class can take care of non-json serializable objects. Another solution is to plug in a custom json encoder/decoder.
class RawField(Field):
    def _to_python(self, value):
        return value

    def _to_json(self, value):
        self._make_json_serializable(value)
        return value

    def _to_json_serializable(self, val):
        if type(val) in (datetime,date,time,Decimal):  # Convert datetime etc to string for JSON serialization
            return str(val)  # Should this be the ISO Format with 'Z' suffix for datetime? http://couchdbkit.org/docs/api/couchdbkit.schema.properties-pysrc.html#value_to_json
        return val

    def _make_json_serializable(self, collection):
        for key in collection:
            if isinstance(collection[key], dict) or isinstance(collection[key], list):
                self._make_json_serializable(collection[key])
            else:
                collection[key] = self._to_json_serializable(collection[key])

  