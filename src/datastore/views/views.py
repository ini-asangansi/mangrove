import os
from datastore import config
from databasemanager.database_manager import DatabaseManager

file_path = os.path.dirname(__file__)

view_names = ["by_location","by_time","by_values"]

def create_views():
    """
    Creates a standard set of views in the database
    """
    database_manager = DatabaseManager(server=config._server,database=config._db)
    for v in view_names:
        if not exists_view(v,database_manager):
            map = open(os.path.join(file_path,v,"map.js")).read()
            reduce = open(os.path.join(file_path,v,"reduce.js")).read()
            database_manager.create_view(v, map, reduce)



def exists_view(aggregation,database_manager):
    entity_type_views = database_manager.load('_design/mangrove_views')
    if entity_type_views and entity_type_views['views'].get(aggregation):
        return True
    return False