from typing import Optional
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,DateField, SelectField, MultipleFileField
from wtforms.fields.core import IntegerField
from wtforms.fields.simple import TextAreaField
from flask_wtf.file import FileAllowed
from wtforms.validators import DataRequired,Email,EqualTo,Optional, Length, NumberRange
from wtforms import ValidationError
from flask_login import current_user
from gitsapp.models import User
from gitsapp import gmap
import os

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
    

        
#Form for Incident report

class CCIEReportForm(FlaskForm):
    first_name = StringField("Crew First Name:", validators=[DataRequired()])
    last_name = StringField("Crew Last Name:", validators=[DataRequired()])
    sup_fname = StringField("Supervisor's First Name:", validators=[DataRequired()])
    sup_lname = StringField("Supervisor's Last Name:", validators=[DataRequired()])
    crew = StringField('Crew ID:', validators=[DataRequired(), Length(4, 4, "Crew ID must be 4 digits")])
    #needs to be empty for now
    date = DateField('Date of Incident',validators=[DataRequired("Please enter a date in the correct format")])
    cleanup = SelectField('Scale of Cleanup:', choices=['Small', 'Moderate', 'Large'])
    building_type = SelectField('Building Type:', choices=building_choices)
    city = StringField('Name of City:', validators=[DataRequired()])
    state = SelectField('State:', choices=state_choices)
    street_address = StringField('Address (No abreviations)',validators=[DataRequired(), validate_address])
    cross_street = StringField('Cross Street (If known):', validators=None)
    zipcode = IntegerField('Zipcode',validators=[DataRequired(), NumberRange(00000, 99999, 'Zipcodes are 5 digits')])
    notes = TextAreaField('Notes',validators=None)
    submit = SubmitField('Create Report')
    photos = MultipleFileField('Upload Photos:', validators=[files_allowed])
    
    

        