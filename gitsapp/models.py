#gitsapp/models.py
#db models for inspector, reporter, reports

from gitsapp import db,login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import date, datetime

#load users for: Reporter and Inspector
@login_manager.user_loader
def load_reporter(reporter_id):
    return Reporter.query.get(reporter_id)

@login_manager.user_loader
def load_inspector(inspector_id):
    return Inspector.query.get(inspector_id)

class Reporter(db.Model, UserMixin):
    
    __tablename__ = 'reporters'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    pwd_hash = db.Column(db.String(128))
    #relationship between reporter and report is one to one
    report = db.relationship('Report', backref='author', lazy=True)
    
    def __init__(self, email, password):
        self.email = email
        self.pwd_hash = generate_password_hash(password)
        
    def check_pwd(self,password):
        return check_password_hash(self.pwhash, password)
    
    def __repr__(self):
        return f"Reporter's Email: {self.email}"
    
class Inspector(db.Model, UserMixin):
    
    __tablename__ = 'inspectors'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64),unique=True, index=True)
    pwd_hash = db.Column(db.String(128))
    #report to inspector is many to many relationship
    
    report = db.relationship('Report',seondary='link')
    
    def __init__(self,email,password):
        self.email = email
        self.pwd_hash = generate_password_hash(password)
        
    def check_pwd(self,password):
        return check_password_hash(self.pwd_hash,password)
    
    def __repr__(self):
        return f"Inspector's email: {self.email}"
    
class Report(db.Model):
    
    __tablename__ = 'report'
    #relationship to reporter, inspector
    reporters = db.relationship(Reporter)
    
    id = db.Column(db.Integer, primary_key=True)
    #connect report to the reporter's id
    reporter_id = db.Column(db.Integer, db.ForeignKey('reporters.id'), nullable=False)
    
    #TODO: connect all the reports to the inspector
    inspector = db.relationship(Inspector,secondary='link')
    supervisor_fname = db.Column(db.String(64), nullable=False)
    supervisor_lname = db.Column(db.String(64), nullable=False)
    crew_id = db.Column(db.Integer, nullable=False)
    date_of_incident = db.Column(db.Datetime,nullable=False,datetime=datetime.utcnow)
    #TODO: scale_cleanup?
    type_of_building = db.Column(db.String(64),nullable=False)
    street_address = db.Column(db.String(256), nullable=False)
    zipcode = db.Column(db.Integer, nullable=False)
    gps_coordinates = db.Column(db.Integer, nullable=False)
    #TODO: image
    notes = db.Column(db.String(256),nullable=False)
    
    def __init__(self, supervisor_fname, supervisor_lname, crew_id, date_of_incident, type_of_building, street_address, zipcode, notes) -> None:
        self.supervisor_fname = supervisor_fname
        self.supervisor_lname = supervisor_lname
        self.crew_id = crew_id
        self.date_of_incident = date_of_incident
        self.type_of_building = type_of_building
        self.street_address = street_address
        self.zipcode = zipcode
        self.notes = notes
    
    def __repr__(self) -> str:
        return f"Zipcode: {self.zipcode}"
    
#Link class to connect many-to-many relationship between reports and Inspectors

class Link(db.Model):
    __tablename__ = 'link'
    report_id = db.Column(db.Integer,ForeignKey='report.id',primary_key=True)
    inspector_id = db.Column(db.Integer,ForeignKey='inspector.id',primary_key=True)
        

