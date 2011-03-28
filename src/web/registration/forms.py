from django import forms
from services.authentication.authentication_service import AuthenticationService

class RegistrationForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'

    title = forms.CharField(max_length=30, required=False)
    first_name = forms.CharField(max_length=30, required=True, label='* First name')
    last_name = forms.CharField(max_length=30,required=True, label='* Last name')
    email = forms.EmailField(required=True, label='* Email')
    confirm_password = forms.CharField(required=True, widget=forms.PasswordInput, label='* Confirm password')
    password = forms.CharField(required=True, widget=forms.PasswordInput, label='* Password')

    organization_name = forms.CharField(required=True, label='* Organization name')
    organization_sector = forms.CharField(widget=(forms.Select(attrs={'class':'width-200px'},choices=(('PublicHealth', 'Public Health'),('Other', 'Other'),))))
    organization_addressline1 = forms.CharField(required=True,max_length=30,label='* Address Line 1')
    organization_addressline2 = forms.CharField(max_length=30, required=False, label='Address Line 2')
    organization_city = forms.CharField(max_length=30,required=True, label='* City')
    organization_state = forms.CharField(max_length=30, required=False, label='State / Province')
    organization_country = forms.CharField(max_length=30,required=True, label='* Country')
    organization_zipcode = forms.CharField(max_length=30,required=True, label='* Postal / Zip Code')
    organization_office_phone = forms.CharField(max_length=30, required=False, label='Office Phone Number')
    organization_website = forms.URLField(required=False, label='Website Url')


    def __init__(self,*args,**kwargs):
        self.authService = AuthenticationService()
        super(RegistrationForm,self).__init__(*args,**kwargs)

    def clean(self):
        # todo cleanup the individual field validations. right now it is throwing some error
        cleaned_data = self.cleaned_data
        if cleaned_data.get('password')\
        != cleaned_data.get('confirm_password'):
            msg = 'Password and Confirm Password do not match.'
            self._errors['password'] = self.error_class([msg])
        user = self.authService.get_user(cleaned_data.get('email'))
        if(user):
            msg = 'Email Id already registered.'
            self._errors['email']=self.error_class([msg])
        return  cleaned_data

    def clean_email(self):
        cleaned_data = self.cleaned_data
        cleaned_data['email']=cleaned_data.get('email').lower()
        return cleaned_data['email']

class LoginForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'

    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)