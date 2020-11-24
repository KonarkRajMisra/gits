#gitsapp/models.py
#db models for inspector, reporter, reports

from gitsapp import db,login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import date, datetime




class User(db.Model, UserMixin):
    
    __tablename__ = 'users'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    __tablename__= 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    pwd_hash = db.Column(db.String(128))
    urole = db.Column(db.String(80))

    def __init__(self, email, password, urole):
        self.email = email
        self.pwd_hash = generate_password_hash(password)
        self.urole = urole
        
    def check_pwd(self,password):
        return check_password_hash(self.pwd_hash, password)
    
    def __repr__(self):
        return f"User's Email: {self.email}"

    

class Report(db.Model):
    
    __tablename__ = 'report'
   

    
    id = db.Column(db.Integer, primary_key=True)
    #connect report to the reporter's id
    #reporter_id = db.Column(db.Integer, db.ForeignKey('reporters.id'), nullable=False)
    
    #TODO: connect all the reports to the inspector
    first_name=db.Column(db.String(64), nullable=False)
    last_name=db.Column(db.String(64), nullable=False)
    supervisor_fname = db.Column(db.String(64), nullable=False)
    supervisor_lname = db.Column(db.String(64), nullable=False)
    crew_id = db.Column(db.Integer, nullable=False)
    date_of_incident = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    scale_of_cleanup = db.Column(db.String(64), nullable=False)
    type_of_building = db.Column(db.String(64),nullable=False)
    street_address = db.Column(db.String(256), nullable=False)
    zipcode = db.Column(db.Integer, nullable=False)
    state = db.Column(db.String(256), nullable=False)
    cross_street = db.Column(db.String(256), nullable=True)

    #TODO: image
    notes = db.Column(db.String(256),nullable=True)

    def __init__(self, first_name, last_name, supervisor_fname, supervisor_lname, crew_id, date_of_incident, scale_of_cleanup, type_of_building, street_address, zipcode, state, cross_street=None, notes=None):
    gps_lat = db.Column(db.Float(2), nullable=False)
    gps_lng = db.Column(db.Float(2), nullable=False)
    #TODO: image
    notes = db.Column(db.String(256),nullable=True)

    def __init__(self, first_name, last_name, supervisor_fname, supervisor_lname, crew_id, date_of_incident, scale_of_cleanup, type_of_building, street_address, zipcode, state,  gps_lat, gps_lng, notes=None, cross_street=None):
        self.first_name = first_name
        self.last_name = last_name
        self.supervisor_fname = supervisor_fname
        self.supervisor_lname = supervisor_lname
        self.crew_id = crew_id
        self.scale_of_cleanup = scale_of_cleanup
        self.date_of_incident = date_of_incident
        self.type_of_building = type_of_building
        self.street_address = street_address
        self.zipcode = zipcode
        self.state = state
        self.cross_street = cross_street
        self.gps_lat = gps_lat
        self.gps_lng = gps_lng
        self.notes = notes
    
    def __repr__(self) -> str:
        return f"Zipcode: {self.zipcode}"
    