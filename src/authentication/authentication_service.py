from authentication.models import EncryptionHelper, UserModel
from services.repository.connection import Connection
from services.repository.repository import Repository

class AuthenticationService(object):
    def __init__(self, repository=Repository(Connection())):
        self.repository = repository

    def create_user(self, userDocument):
        return self.repository.save(userDocument)

    def authenticate_user(self, email, password):
        user = self.repository.load(email, UserModel)
        if user and EncryptionHelper().check_password(user.password, password):
            return user
        return None

    def get_user(self, email):
        user = self.repository.load(email, UserModel)
        return user
    
        
  