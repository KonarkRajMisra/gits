from typing import Optional
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,DateField, SelectField
from wtforms.fields.core import IntegerField
from wtforms.fields.simple import TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired,Email,EqualTo,Optional, Length
from wtforms import ValidationError
from flask_login import current_user
from gitsapp.models import User

building_choices = [
    'Residential',
    'Educational',
    'Institutional',
    'Assembly',
    'Business',
    'Mercantile',
    'Industrial',
    'Storage',
    'Unsafe',
    'Special',
    'Car Parking'
]

state_choices = [
    'Alabama',
    'Alaska',
    'Arizona',
    'Arkansas',
    'California',
    'Colorado',
    'Connecticut',
    'Delaware',
    'District Of Columbia',
    'Florida',
    'Georgia',
    'Hawaii',
    'Idaho',
    'Illinois',
    'Indiana',
    'Iowa',
    'Kansas',
    'Kentucky',
    'Louisiana',
    'Maine',
    'Maryland',
    'Massachusetts',
    'Michigan',
    'Minnesota',
    'Mississippi',
    'Missouri',
    'Montana',
    'Nebraska',
    'Nevada',
    'New Hampshire',
    'New Jersey',
    'New Mexico',
    'New York',
    'North Carolina',
    'North Dakota',
    'Ohio',
    'Oklahoma',
    'Oregon',
    'Pennsylvania',
    'Rhode Island',
    'South Carolina',
    'South Dakota',
    'Tennessee',
    'Texas',
    'Utah',
    'Vermont',
    'Virginia',
    'Washington',
    'West Virginia',
    'Wisconsin',
    'Wyoming'
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
        
#Form for Incident report

class CCIEReportForm(FlaskForm):
    first_name = StringField("Crew First Name:", validators=[DataRequired()])
    last_name = StringField("Crew Last Name:", validators=[DataRequired()])
    sup_fname = StringField("Supervisor's First Name:", validators=[DataRequired()])
    sup_lname = StringField("Supervisor's Last Name:", validators=[DataRequired()])
    crew = StringField('Crew ID:', validators=[DataRequired(), Length(4, 4, "Crew ID must be 4 digits")])
    date = DateField('Date of Incident',validators=[DataRequired()])
    cleanup = SelectField('Scale of Cleanup:', choices=['Small', 'Moderate', 'Large'])
    building_type = SelectField('Building Type:', choices=building_choices)
    city = StringField('Name of City:', validators=[DataRequired()])
    state = SelectField('State:', choices=state_choices)
    street_address = StringField('Address (No abreviations)',validators=[DataRequired()])
    cross_street = StringField('Cross Street (If known):', validators=None)
    zipcode = IntegerField('Zipcode',validators=[DataRequired()])
    notes = TextAreaField('Notes',validators=None)
    submit = SubmitField('Create Report')
    photo = FileField('Upload Photo', validators=[FileAllowed(['jpg', 'png', 'PNG'], 'Images only!')])
    
    

        