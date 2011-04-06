from datastore.database import get_db_manager
import bylocation, byvalues, bytime

view_js = {
    'by_location': (bylocation._map, bylocation._reduce),
    'by_time': (bytime._map, bytime._reduce),
    'by_values': (byvalues._map, byvalues._reduce)
}

def create_views():
    """
    Creates a standard set of views in the database
    """
    database_manager = get_db_manager()
    for v in view_js.keys():
        if not exists_view(v,database_manager):
            database_manager.create_view(v, view_js[v][0], view_js[v][1])



def exists_view(aggregation,database_manager):
    entity_type_views = database_manager.load('_design/mangrove_views')
    if entity_type_views and entity_type_views['views'].get(aggregation):
        return True
    return False