from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,DecimalField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError
from wtforms.fields.html5 import DateField
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


#Form for LEGI report
class LegiReportForm(FlaskForm):
    pass

class GaReportForm(FlaskForm):
    start_date = DateField('Start Date', format='%m/%d/%Y')
    end_date = DateField('End Date', format='%m/%d/%Y')
    start_gps_lat = DecimalField('Start Latitude')
    start_gps_lng = DecimalField('Start Longitude')
    end_gps_lat = DecimalField('End Latitude')
    end_gps_lng = DecimalField('End Longitude')
    submit = SubmitField('Submit')
    suspect_name = StringField('Suspect Name')
    gang_name = StringField('Gang or Crew Name')
    day_thresh = DecimalField('Day Threshold')
    coord_thresh_lat = DecimalField('Latitude Threshold')
    coord_thresh_lng = DecimalField('Longitude Threshold')
    mile_range = DecimalField("Mile Range")
    calc = SubmitField('Calculate')
    
    
    