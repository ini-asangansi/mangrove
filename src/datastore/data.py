# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from datastore.database import get_db_manager
from utils import utcnow

# Return result as { "Health_Facility.Clinic" : [("beds" ,"avg",200), ("meds" ,"sum",320)  ] })
def fetch(dbm,entity_type,aggregates= {},aggregate_on = {},starttime=None,endtime=None,filter=None):
    result = []
    values = _get_latest_values(dbm,entity_type)
    for field,aggregate in aggregates.items():
        val = _calc_aggregate(aggregate,values[field])
        result.append( (field, aggregate, val) )
    return  {  ".".join(entity_type) :  result }

# Returns the list of latest values per field across entities of the given type.
# E.g {'beds': [400, 200, 300, 300, 400, 200], 'meds': [450, 50, 20, 20, 450, 50], 'doctors': [10, 5, 2, 2, 10, 5]}
def _get_latest_values(dbm,type_path):
    view_name = "by_values"
    rows = dbm.load_all_rows_in_view('mangrove_views/'+ view_name, group_level=3,
                                                 startkey=[type_path],
                                                 endkey=[type_path,{}])
    values = {}
    for row in rows:
        f = row['value']['field']
        v = row['value']['value']
        values.setdefault(f,[]).append(v)
    return values

# Accepts a list of values and applies aggregation over that list.
def _calc_aggregate(aggregate,values):
    if aggregate == "sum":
        return sum(values)
    elif aggregate == "avg":
        return sum(values)/len(values)

# The below does the aggregation in couch instead of in python.
def _get_aggregate_value_(type_path,field_name, aggregate_fn,date):
    view_name = "by_time"
    _dbm = get_db_manager('http://localhost:5984/', 'mangrove-test')
    rows = _dbm.load_all_rows_in_view('mangrove_views/'+ view_name, group_level=2,descending=False,
                                                 startkey=[type_path,field_name],
                                                 endkey=[type_path, field_name,{}])
    # The above will return rows in the format described:
    #        [<Row key=[['Health_Facility', 'Clinic'], 'meds'], value={'count': 3, 'max': 250, 'sum': 320, 'min': 20, 'sumsqr': 65400}>]
    if len(rows):
        if aggregate_fn == "avg":
            total =  rows[0]['value']['sum']
            count =  rows[0]['value']['count']
            val = total/count
        else:
            val = rows[0]['value'][aggregate_fn]
        return val
    else:
        return None
