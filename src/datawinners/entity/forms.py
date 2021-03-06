from django.core.exceptions import ValidationError
from django.forms.fields import RegexField, CharField, FileField
from django.forms.forms import Form
from mangrove.utils.types import is_empty

class EntityTypeForm(Form):
    error_css_class = 'error'
    required_css_class = 'required'

    entity_type = RegexField(regex="^[A-Za-z0-9]+$", max_length=20, error_message="Only letters and numbers are valid", required=True, label="New Subject(eg clinic, waterpoint etc)")

class ReporterRegistrationForm(Form):
    error_css_class = 'error'
    required_css_class = 'required'

    first_name = RegexField(regex="[^0-9.,\s@#$%&*~]*", max_length=20,
                            error_message="Please enter a valid value containing only letters a-z or A-Z or symbols '`- "
                            ,
                            label="* Name")
    telephone_number = RegexField(required=True, regex="^\d+(-\d+)*$", max_length=15, label="* Mobile Number",
                                  error_message="Please enter a valid phone number")
    geo_code = CharField(max_length=30, required=False, label="GPS: Enter Lat Long")
    location = CharField(max_length=30, required=False, label="Enter location")


    def clean_geo_code(self):
        geo_code_string = self.cleaned_data['geo_code']
        geo_code_string = geo_code_string.strip()
        geo_code_string = (' ').join(geo_code_string.split())
        if is_empty(geo_code_string):
            return geo_code_string
        lat_long = geo_code_string.split(' ')
        if len(lat_long) != 2:
            raise ValidationError("GPS coordinates must be in the format 'lat long'.")
        if not (-90 < float(lat_long[0]) < 90 and -180 < float(lat_long[1]) < 180):
            raise ValidationError("Incorrect GPS coordinates. Please resubmit.")
        return geo_code_string

    def clean(self):
        a = self.cleaned_data.get("location")
        b = self.cleaned_data.get("geo_code")
        if not (bool(a) or bool(b)):
            raise ValidationError("Required information for registration. Please fill out at least one location field correctly.")
        return self.cleaned_data


class SubjectUploadForm(Form):
    error_css_class = 'error'
    required_css_class = 'required'
    file = FileField(label='Import Subjects')