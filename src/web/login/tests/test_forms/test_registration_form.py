from services.authentication.authentication_service import AuthenticationService
from services.authentication.models import UserModel
from web.login.forms import RegistrationForm
from mock import Mock


class TestRegistrationForm:
    def setup(self):
        pass

    def teardown(self):
        pass

    def test_email_is_converted_to_lower_case(self):
        base_form = {'first_name':'a',
                     'last_name':'b',
                     'email':'A@b.com',
                     'password':'a','confirm_password':'a', 'organization_name':'ad','organization_addressline1':'asa','organization_city':'aaa','organization_country':'aa','organization_zipcode':'asd'
                     ,'organization_sector':'Other'}
        r = RegistrationForm(base_form)
        r.is_valid()
        print r._errors
        assert r.cleaned_data.get('email') == 'a@b.com'


    def test_email_should_be_unique(self):
        authenticationService = Mock(spec=AuthenticationService)
        email_id = 'A@b.com'
        authenticationService.get_user.return_value = UserModel(email=email_id)
        base_form = {'first_name':'a',
                     'last_name':'b',
                     'email':email_id,
                     'password':'a','confirm_password':'a', 'organization_name':'ad','organization_addressline1':'asa','organization_city':'aaa','organization_country':'aa','organization_zipcode':'asd'
                     ,'organization_sector':'Other'}
        r = RegistrationForm(base_form)
        r.authService = authenticationService
        r.is_valid()
        assert r._errors['email'] == r.error_class(['Email Id already registered.'])


    def test_password_and_confirm_password_match(self):
        base_form = {'first_name':'a',
                     'last_name':'b',
                     'email':'A@b.com',
                     'password':'a','confirm_password':'a', 'organization_name':'ad','organization_addressline1':'asa','organization_city':'aaa','organization_country':'aa','organization_zipcode':'asd'
                     ,'organization_sector':'Other'}
        r = RegistrationForm(base_form)
        assert r.is_valid()

    def test_error_when_password_and_confirm_password_do_not_match(self):
        base_form = {'first_name':'a',
                     'last_name':'b',
                     'email':'A@b.com',
                     'password':'a','confirm_password':'b', 'organization_name':'ad','organization_addressline1':'asa','organization_city':'aaa','organization_country':'aa','organization_zipcode':'asd'
                     ,'organization_sector':'Other'}
        r = RegistrationForm(base_form)
        assert not r.is_valid()
        assert r._errors['password'] == r.error_class(['Password and Confirm Password do not match.'])

    

