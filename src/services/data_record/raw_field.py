import json
from couchdb.mapping import Field

class RawField(Field):
    def _to_python(self, value):
        return value

    def _to_json(self, value):
        self.fix_collection(value)
        return value

    def fix_collection(self, collection):
        for key in collection:
            if isinstance(collection[key], dict) or isinstance(collection[key], list):
                self.fix_collection(collection[key])
            else:
                collection[key] = str(collection[key])
  