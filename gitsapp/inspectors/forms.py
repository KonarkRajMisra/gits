from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,SelectField,IntegerField, MultipleFileField
from flask_wtf.file import FileAllowed
from wtforms.validators import DataRequired,Email,EqualTo
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
class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message="Passwords must match!")])
    pass_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')
    
    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('User already exists. Please Log In.')


#Form for LEGI report
class LegiReportForm(FlaskForm):
    type_of_building = SelectField('Building Type:', choices=['No Change', 'Residential', 'Educational', 'Institutional', 'Assembly', 'Business', 'Mercantile', 'Industrial', 'Storage', 'Unsafe', 'Special', 'Car Parking'])
    moniker = StringField('Moniker (If known):', validators=None)
    street_address = StringField('Address (No abbreviations):',validators=[DataRequired()])
    zipcode = IntegerField('Zipcode:',validators=[DataRequired()])
    cross_street = StringField('Cross Street (If known):', validators=None)
    cleanup = SelectField('Scale of Cleanup (Damage):', choices=['No Change', 'Small', 'Moderate', 'Large'])
    investigation_status = SelectField('Status of Investigation:', choices=['No Change', 'New', 'In Process', 'In litigation', 'Resolved'])
    new_photos = MultipleFileField('Add Photos:', validators=[FileAllowed(['jpg', 'png', 'PNG'], 'Images only!')])
    submit = SubmitField('Submit')

class SearchSuspectForm(FlaskForm):
    first_name = StringField('Suspect First Name (If Known):', validators=None)
    last_name = StringField('Suspect Last Name (If Known):', validators=None)
    submit = SubmitField('Look Up Suspect')

class SuspectForm(FlaskForm):
    first_name = StringField('Suspect First Name (If Known):', validators=None)
    last_name = StringField('Suspect Last Name (If Known):', validators=None)
    gang = StringField('Gang Affiliation(If Known):', validators =None)
    status = SelectField('Status of suspect:', choices=['No Change', 'Unknown', 'Identified', 'In Custody', 'Released'])
    sus_photos = MultipleFileField('Add Photos:', validators=[FileAllowed(['jpg', 'png', 'PNG'], 'Images only!')])
    submit = SubmitField('Create/Update Suspect')

