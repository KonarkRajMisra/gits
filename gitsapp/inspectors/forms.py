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
    building_type = SelectField('Building Type:', choices=building_choices)
    moniker = StringField('Moniker (If known):', validators=None)
    street_address = StringField('Address:',validators=[DataRequired()])
    zipcode = IntegerField('Zipcode:',validators=[DataRequired()])
    cross_street = StringField('Cross Street (If known):', validators=None)
    cleanup = SelectField('Scale of Cleanup (Damage):', choices=['Small', 'Moderate', 'Large'])
    investigation_status = SelectField('Status of Investigation:', choices=['New', 'In Process', 'In litigation', 'Resolved'])
    new_photos = MultipleFileField('Add Photos:', validators=[FileAllowed(['jpg', 'png', 'PNG'], 'Images only!')])
    submit = SubmitField('Edit Report')

class SuspectForm(FlaskForm):
    first_name = StringField('Suspect First Name (If Known):', validators=None)
    last_name = StringField('Suspect Last Name (If Known):', validators=None)
    gang = StringField('Suspect Gang Affiliation (If Known):', validators =None)
    status = SelectField('Status of suspect:', choices=['Unknown', 'Identified', 'In Custody', 'Released'])

