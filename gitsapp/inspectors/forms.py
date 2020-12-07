from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,SelectField,IntegerField, MultipleFileField
from flask_wtf.file import FileAllowed
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import StringField,PasswordField,SubmitField,SelectField
from wtforms.validators import DataRequired,Email,EqualTo, Length, NumberRange
from wtforms import ValidationError
from gitsapp.reporters.forms import building_choices

from flask_login import current_user
from gitsapp.models import User

cleanup_choice = [
    'Small',
    'Moderate',
    'Large'
]

invest_status = [
    'New',
    'In Process',
    'In Litigation',
    'Resolved'
]

suspect_status = [
    'Unknown',
    'Identified',
    'In Custody',
    'Released'
]

allowed_exts = ['.jpg', '.png', '.jpeg']

def files_allowed(form,field):
    for file in field.data:
        file_name, extension = os.path.splitext(file.filename)

        if extension.lower() not in allowed_exts:
            raise ValidationError('File not allowed. Images only!')

def validate_email(form,field):
    if User.query.filter_by(email=field.data).first():
        raise ValidationError('User already exists. Please Log In.')

def validate_address(form, field):
    #Find GPS coordinates
    result = gmap.geocode(field.data)
    #basic check to make sure address matches state
    try:
        if(result == None or result[0].get("address_components")[5].get("long_name") != form.state.data):
            raise ValidationError('Address does not match the state provided. Ensure the address entered has no abbreviations (Ex. Drive not Dr. )')

    except:
         raise ValidationError('Address does not match the state provided. Ensure the address entered has no abbreviations (Ex. Drive not Dr. )')


class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email(), validate_email])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message="Passwords must match!"), Length(6,24, "Password must be 6-24 characters long")])
    pass_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')
    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('User already exists. Please Log In.')


#Form for LEGI report
class LegiReportForm(FlaskForm):
    type_of_building = SelectField('Building Type:', choices=['No Change', 'Residential', 'Educational', 'Institutional', 'Assembly', 'Business', 'Mercantile', 'Industrial', 'Storage', 'Unsafe', 'Special', 'Car Parking'])
    moniker = StringField('Moniker (If known):', validators=None)
    street_address = StringField('Address (No abbreviations):',validators=[DataRequired(), validate_address])
    zipcode = IntegerField('Zipcode:',validators=[DataRequired(), NumberRange(00000, 99999, 'Zipcodes are 5 digits')])
    cross_street = StringField('Cross Street (If known):', validators=None)
    cleanup = SelectField('Scale of Cleanup (Damage):', choices=['No Change', 'Small', 'Moderate', 'Large'])
    investigation_status = SelectField('Status of Investigation:', choices=['No Change', 'New', 'In Process', 'In litigation', 'Resolved'])
    new_photos = MultipleFileField('Add Photos:', validators=[FileAllowed(['jpg', 'png', 'PNG'], 'Images only!')])
    submit = SubmitField('Submit')

class SearchForm(FlaskForm):
    search = StringField('search', [DataRequired()])
    submit = SubmitField('Search Report')
    cleanup = SelectField('Scale of Cleanup (Damage):', choices=['No Change', 'Small', 'Moderate', 'Large'])
    investigation_status = SelectField('Status of Investigation:', choices=['No Change', 'New', 'In Process', 'In litigation', 'Resolved'])
    new_photos = MultipleFileField('Add Photos:', validators=[FileAllowed(['jpg', 'png', 'PNG'], 'Images only!')])
    submit = SubmitField('Submit')

class SearchSuspectForm(FlaskForm):
    search_first_name = StringField('Suspect First Name (If Known):', validators=None)
    search_last_name = StringField('Suspect Last Name (If Known):', validators=None)
    submit = SubmitField('Look Up Suspect')

class SuspectForm(FlaskForm):
    first_name = StringField('Suspect First Name (If Known):', validators=None)
    last_name = StringField('Suspect Last Name (If Known):', validators=None)
    gang = StringField('Gang Affiliation(If Known):', validators =None)
    status = SelectField('Status of suspect:', choices=['No Change', 'Unknown', 'Identified', 'In Custody', 'Released'])
    sus_photos = MultipleFileField('Add Photos:', validators=[files_allowed])
    submit = SubmitField('Create/Update Suspect')


class GraffitiAnalysisForm(FlaskForm):
    start_date = StringField('Start Date', validators=[DataRequired()])
    end_date = StringField('End Date', validators=[DataRequired()])
    start_gps_lat = StringField('Starting Date GPS Latitude Coordinates', validators=None)
    start_gps_lng = StringField('Starting Date GPS Latitude Coordinates', validators=None)
    end_gps_lat = StringField('Ending Date GPS Latitude Coordinates', validators=None)
    end_gps_lng = StringField('Ending Date GPS Longitude Coordinates', validators=None)
    suspect_name = StringField('Suspect Name', validators=None)
    gang_name = StringField('Gang Name', validators=None)
    calculate = SubmitField('Calculate')


