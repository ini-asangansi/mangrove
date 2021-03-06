# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from mangrove.datastore.data import EntityAggregration

from mangrove.errors.MangroveException import NumberNotRegisteredException
from mangrove.datastore import data
from mangrove.form_model.form_model import MOBILE_NUMBER_FIELD, NAME_FIELD, SHORT_NAME_FIELD

REPORTER_ENTITY_TYPE = ["reporter"]


def find_reporter(dbm, from_number):
    from_reporter_list = get_reporter_by_from_number(dbm, from_number)
    return [each.values()[0] for each in from_reporter_list]

def get_short_code_from_reporter_number(dbm, from_number):
    from_reporter_list = get_reporter_by_from_number(dbm, from_number)
    return from_reporter_list[0].keys()[0].split('/')[1]

def get_reporter_by_from_number(dbm, from_number):
    reporters = data.aggregate(dbm, entity_type=["reporter"],
                            aggregates={MOBILE_NUMBER_FIELD: data.reduce_functions.LATEST,
                                        NAME_FIELD: data.reduce_functions.LATEST},aggregate_on=EntityAggregration()
                          )
    from_reporter_list = [{x:reporters[x]} for x in reporters if reporters[x].get(MOBILE_NUMBER_FIELD) == from_number]
    if not len(from_reporter_list):
        raise NumberNotRegisteredException(from_number)
    return from_reporter_list