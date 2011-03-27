from datetime import datetime
import re
from services.authentication.models import UserModel, EncryptionHelper

class TestUserModel(object):

    def test_should_create_user_model(self):
        user = UserModel(id='TestUser1',title='Mr.',first_name='Test',last_name='User',email='testuser1@email.com', password = 'password', organization_id = 'org_id')
        assert user.id == 'TestUser1'
        assert user.title == 'Mr.'
        assert user.first_name=='Test'
        assert user.last_name=='User'
        assert user.email=='testuser1@email.com'
        assert re.match('.*\$.*\$.*',  user.password)
        assert user.organization_id == 'org_id'

    def test_should_encrypt_password_for_user(self):
        user = UserModel(password = 'password')
        assert EncryptionHelper().check_password(user.password, 'password')

    def test_username_should_be_same_as_email(self):
        user = UserModel(id='testuser1@email.com', email='testuser1@email.com')
        assert user.username == user.email

