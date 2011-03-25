from django.contrib.auth.models import User
from services.authentication.authentication_service import AuthenticationService
from services.repository.connection import Connection
from services.repository.repository import Repository

class AuthenticationBackend(object):
    """
    Authenticates against services.authentication.UserModel
    """
    supports_object_permissions = False
    supports_anonymous_user = False

    # TODO: Model, login attribute name and password attribute name should be
    # configurable.
    def authenticate(self, username=None, password=None):
        user = AuthenticationService().authenticate_user(email=username, password=password)
        return user

    def get_group_permissions(self, user_obj):
        """
        Returns a set of permission strings that this user has through his/her
        groups.
        """
        return []

    def get_all_permissions(self, user_obj):
        return []

    def has_perm(self, user_obj, perm):
        return True

    def has_module_perms(self, user_obj, app_label):
        """
        Returns True if user_obj has any permissions in the given app_label.
        """
        return True

    def get_user(self, user_id):
        return AuthenticationService().get_user(user_id)

