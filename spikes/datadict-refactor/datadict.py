# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from datastore.database import DatabaseManager
from documents import DataDictDocument
from utils import is_string

class DataDictType(object):
    '''DataDict is an abstraction that stores named data types and constraints .'''

    def __init__(self, dbm, name, data_type, description, constraints=None, _document=None):
        '''Create a new DataDictType.

        This represents a type of data that can be used to coordinate data collection and interoperability.
        '''
        assert isinstance(dbm, DatabaseManager)
        assert _document is not None or is_string(name)
        assert _document is not None or is_string(data_type)
        assert _document is not None or description is None or is_string(description)
        assert _document is not None or constraints is None or isinstance(constraints, dict)
        assert _document is None or isinstance(_document, DataDictDocument)

        self._dbm = dbm

        # Are we being constructed from an existing doc?
        if _document is not None:
            self._doc = _document
            return

        # Not made from existing doc, so create a new one
        self._doc = DataDictDocument(name, data_type, description, constraints)