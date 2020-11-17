from typing import Optional
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,DateField
from wtforms.fields.core import IntegerField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired,Email,EqualTo,Optional
from wtforms import ValidationError

from flask_login import current_user
from gitsapp.models import User


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
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    crew = IntegerField('Crew Id', validators=[Optional()])
    #needs to be empty for now
    date = DateField('Date of Incident',validators=[Optional()])
    building_type = StringField('Type of Building', validators=None)
    street_address = StringField('Address',validators=None)
    zipcode = IntegerField('Zipcode',validators=[DataRequired()])
    notes = TextAreaField('Notes',validators=None)
    submit = SubmitField('Create Report')
    
    
    
        