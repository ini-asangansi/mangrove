__author__ = 'root'


__all__ = ['put','of']


def put(identifier, data_id):
    return data_id[identifier]

def of(data_id):
    return data_id