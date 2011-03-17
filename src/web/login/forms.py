from django import forms

class RegistrationForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'

    title = forms.CharField(max_length=30, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30,required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)
    confirm_password = forms.CharField(required=True, widget=forms.PasswordInput)
    organization_name = forms.CharField(required=True)
    organization_sector = forms.CharField(widget=(forms.Select(attrs={'class':'width-200px'},choices=(('Public Health', 'PublicHealth'),('Other', 'Other'),))))
    organization_addressline1 = forms.CharField(max_length=30, label='Address Line 1')
    organization_addressline2 = forms.CharField(max_length=30, label='Address Line 2')
    organization_city = forms.CharField(max_length=30,required=True, label='City')
    organization_state = forms.CharField(max_length=30, label='State / Province')
    organization_country = forms.CharField(max_length=30,required=True, label='Country')
    organization_zipcode = forms.CharField(max_length=30,required=True, label='Postal / Zip Code')
    organization_office_phone = forms.CharField(max_length=30, label='Office Phone Number')
    organization_website = forms.URLField(label='Website Url')

    def clean(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('password') != cleaned_data.get('confirm_password'):
            raise forms.ValidationError('Password and Confirm Password do not match.')
        return  cleaned_data


    