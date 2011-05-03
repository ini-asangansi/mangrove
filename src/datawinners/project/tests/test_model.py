import unittest
from datawinners.project.models import Project, get_all_projects, get_project
from mangrove.datastore.database import get_db_manager, _delete_db_and_remove_db_manager
from datawinners.main.management.commands.recreateviews import create_views

class TestProjectModel(unittest.TestCase):
    def setUp(self):
        self.dbm = get_db_manager(database='mangrove-test')
        create_views(self.dbm)
        project1 = Project(name="Test1", goals="Testing", project_type="Survey", entity_type="Clinic", devices=['web'])
        self.project1_id = project1.save(self.dbm).id
        project2 = Project(name="Test2", goals="Testing", project_type="Survey", entity_type="Clinic", devices=['web'])
        self.project2_id = project2.save(self.dbm).id

    def tearDown(self):
        _delete_db_and_remove_db_manager(self.dbm)

    def test_get_all_projects(self):
        projects = get_all_projects(self.dbm)
        self.assertEquals(len(projects), 2)

    def test_get_one_project(self):
        self.assertEquals(get_project(self.project1_id,self.dbm)['_id'], self.project1_id)