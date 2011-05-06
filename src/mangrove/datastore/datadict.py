# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from mangrove.datastore.database import DatabaseManager
from mangrove.datastore.documents import DataDictDocument
from mangrove.utils.types import is_string

# Temporary stuff, till datadict is fully implemented in datawinners : Aroj


def get_default_datadict_type():
    return DataDictType(DatabaseManager(), name='Default Datadict Type', slug='default', primitive_type='string')


def get_datadict_type(dbm, uuid):
    assert isinstance(dbm, DatabaseManager)
    datadict_doc = dbm.load(uuid, DataDictDocument)
    return DataDictType(dbm, _document=datadict_doc)


def get_datadict_types(dbm, uuids):
    return [get_datadict_type(dbm, i) for i in uuids]


class DataDictType(object):
    '''DataDict is an abstraction that stores named data types and constraints .'''

    def __init__(self, dbm, name=None, slug=None, primitive_type=None, description=None, \
                 constraints=None, tags=None, id=None, _document=None, **kwargs):
        '''Create a new DataDictType.

        This represents a type of data that can be used to coordinate data collection and interoperability.
        '''
        assert isinstance(dbm, DatabaseManager)
        assert _document is not None or is_string(name)
        assert _document is not None or is_string(slug)
        assert _document is not None or is_string(primitive_type)
        assert _document is not None or description is None or is_string(description)
        assert _document is not None or constraints is None or isinstance(constraints, dict)
        assert _document is None or isinstance(_document, DataDictDocument)
        # how to assert any kwargs?

        self._dbm = dbm

        # Are we being constructed from an existing doc?
        if _document is not None:
            self._doc = _document
            return

        # Not made from existing doc, so create a new one
        self._doc = DataDictDocument(id, primitive_type, constraints, slug, name, description, tags, **kwargs)

    def save(self):
        return self._dbm.save(self._doc).id

    @property
    def id(self):
        return self._doc.id

    @property
    def name(self):
        return self._doc.name

    @property
    def slug(self):
        return self._doc.slug

    @property
    def description(self):
        return self._doc.description

    @property
    def constraints(self):
        return self._doc.constraints

    @property
    def primitive_type(self):
        return self._doc.primitive_type

    @property
    def tags(self):
        return self._doc.tags
