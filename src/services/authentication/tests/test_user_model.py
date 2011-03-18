from datetime import datetime
import re
from services.authentication.models import UserModel, EncryptionHelper

class TestUserModel:

    def test_should_create_user_model(self):
        user = UserModel(id='TestUser1',title='Mr.',first_name='Test',last_name='User',email='testuser1@email.com', password = 'password')
        assert (datetime.utcnow() - user.created_on).total_seconds() < 10
        assert user.id == 'TestUser1'
        assert user.title == 'Mr.'
        assert user.first_name=='Test'
        assert user.last_name=='User'
        assert user.email=='testuser1@email.com'
        assert re.match('.*\$.*\$.*',  user.password)

    def test_should_encrypt_password_for_user(self):
        user = UserModel(password = 'password')
        print user.password
        assert EncryptionHelper().check_password(user.password, 'password')

