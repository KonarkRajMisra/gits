from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,SelectField
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
    street_address = StringField('Address',validators=[DataRequired()])
    cross_street = StringField('Cross Street (If known):', validators=None)
    moniker = StringField('Moniker',validators=[DataRequired()])
    sus_fname = StringField('Suspect First Name',validators=[DataRequired()])
    sus_lname = StringField('Suspect Last Name',validators=[DataRequired()])
    gang_name = StringField('Gang or Crew Name',validators=[DataRequired()])
    cleanup_type = SelectField('Amount of Cleanup:', choices=cleanup_choice)
    building_type = SelectField('Investigation Status:', choices=invest_status)
    building_type = SelectField('Suspect Status:', choices=suspect_status)
    #TODO: gps_coordinates
    #TODO: images
    submit = SubmitField('Edit Report')