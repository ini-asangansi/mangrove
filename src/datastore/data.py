# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from datastore.database import get_db_manager
from utils import utcnow

#{ "Health_Facility.Clinic" : [("beds" ,"avg",200), ("meds" ,"sum",320)  ] })
def fetch(entity_type,aggregates= {},aggregate_on = {},starttime=None,endtime=None,filter=None):
    values = []
    for field,aggregate in aggregates.items():
        val = _get_aggregate_value(entity_type,field,aggregate,utcnow())
        values.append( (field, aggregate, val) )
    return  {  ".".join(entity_type) :  values }

def _get_aggregate_value(type_path,field_name, aggregate_fn,date):
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
