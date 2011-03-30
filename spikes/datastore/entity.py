import uuid
import couchdb
import datetime

# Module (almost Class) methods

def get_by_id(id):
    """
    returns an entity from the given entity id
    """
    return None

def get_by_type(type):
    """
    returns a list of entities that match the given type
    """
    return []

def get_by_attribute(attribute=[]):
    """
    returns a list of entities that match the given attributes
    """
    return []

# Main Entity class

class Entity(object):

    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    def save(self):
        pass

    def update(self, **kwargs):
        pass

    def delete(self):
        pass

    def add_data(self, record):
        pass

    def update_data(self, record):
        pass

    def invalidate_data(self, record):
        pass

    def get_data(self):
        pass
