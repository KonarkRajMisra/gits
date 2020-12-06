#gitsapp/models.py
#db models for inspector, reporter, reports

from gitsapp import db,login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import date, datetime





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
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
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
    gps_lat = db.Column(db.Float(2), nullable=False)
    gps_lng = db.Column(db.Float(2), nullable=False)
    notes = db.Column(db.String(256),nullable=True)
    investigation_status = db.Column(db.String(64), nullable=True)      
    images = db.relationship('Report_Image', backref='report', lazy=True)
    is_hotspot = db.Column(db.Boolean,nullable=False)
    suspect = db.relationship('Suspect', backref=db.backref('report', lazy=True))

        

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
    

    def has_keyword(self, keyword):
        if (keyword in str.lower(self.first_name)) or (keyword in str.lower(self.last_name)) or (keyword in str.lower(self.supervisor_fname)) or (keyword in str.lower(self.supervisor_lname)) or (keyword in str.lower(str(self.crew_id))) or (keyword in str.lower(self.scale_of_cleanup)) or (keyword in str.lower(self.type_of_building)) or (keyword in str.lower(self.street_address)) or (keyword in str.lower(str(self.zipcode))) or (keyword in str.lower(self.state)) or (keyword in str.lower(self.cross_street)) or (keyword in str.lower(str(self.gps_lat))) or (keyword in str.lower(str(self.gps_lng))) or (keyword in str.lower(str(self.notes))):
            return True
        return False

class Suspect(db.Model):

    __tablename__ = 'suspect'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    gang = db.Column(db.String(128), nullable=True)
    status = db.Column(db.String(64), nullable=True)
    #images = db.relationship('Suspect_Image', backref='suspect', lazy=True)
    report_id = db.Column(db.Integer, db.ForeignKey('report.id'))

    def __init__(self, first_name, last_name, gang=None, status="Unknown"):
        self.first_name = first_name
        self.last_name = last_name
        self.gang = gang
        self.status = status

    def __repr__(self) -> str:
        return f"Name: {self.first_name}"
    def has_keyword(self, keyword):
        if (keyword in str.lower(self.first_name)) or (keyword in str.lower(self.last_name)) or (keyword in str.lower(self.supervisor_fname)) or (keyword in str.lower(self.supervisor_lname)) or (keyword in str.lower(str(self.crew_id))) or (keyword in str.lower(self.scale_of_cleanup)) or (keyword in str.lower(self.type_of_building)) or (keyword in str.lower(self.street_address)) or (keyword in str.lower(str(self.zipcode))) or (keyword in str.lower(self.state)) or (keyword in str.lower(self.cross_street)) or (keyword in str.lower(str(self.gps_lat))) or (keyword in str.lower(str(self.gps_lng))) or (keyword in str.lower(str(self.notes))):
            return True
        return False
