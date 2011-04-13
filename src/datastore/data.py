# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from datastore.database import get_db_manager
from utils import utcnow

def fetch(dbm,entity_type,aggregates= {},aggregate_on = {},starttime=None,endtime=None,filter=None):
    result = {}
    values = _load_all_fields_aggregated(dbm,entity_type)
    print values
    for val in values:
        entity_id = val["entity_id"]
        field = val["field"]
        if field in aggregates:
            interested_aggregate = aggregates[field]
            result.setdefault(entity_id,{})[field] = val[interested_aggregate]
    return result

# Returns list of dicts
#           {'count': 2, 'entity_id': 'a5ab88e9131947f9a44b392a30e5ce64', 'timestamp': 1298937600000L, 'sum': 800, 'field': 'beds', 'latest': 500},
#           {'count': 1, 'entity_id': 'a5ab88e9131947f9a44b392a30e5ce64', 'timestamp': 1296518400000L, 'sum': '0Dr. A', 'field': 'director', 'latest': 'Dr. A'},
#           {'count': 2, 'entity_id': 'a5ab88e9131947f9a44b392a30e5ce64', 'timestamp': 1298937600000L, 'sum': 30, 'field': 'patients', 'latest': 20},
def _load_all_fields_aggregated(dbm,type_path):
    view_name = "by_values"
    rows = dbm.load_all_rows_in_view('mangrove_views/'+ view_name, group_level=3,
                                                 startkey=[type_path],
                                                 endkey=[type_path,{}])
    values = []
    for row in rows:
        values.append(row['value'])
    return values

