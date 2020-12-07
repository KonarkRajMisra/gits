from gitsapp.models import User, db, Report, Suspect
from gitsapp.reporters.forms import RegistrationForm
from gitsapp import app
from flask import template_rendered
import pytest

@pytest.fixture(scope='module')
def new_reporter():
    User.__table__.drop(db.engine)
    db.create_all()
    user = User('reporter@test.com', '12345678', 'WORKER')
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture(scope='module')
def new_inspector():
    User.__table__.drop(db.engine)
    db.create_all()
    user = User('inspector@test.com', '12345678', 'LAW')
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture(scope='module')
def test_client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client

@pytest.fixture(scope='module')
def login_reporter(test_client, new_reporter):
    test_client.post('/login_reporter', data=dict(email=new_reporter.email,password='12345678'))


@pytest.fixture(scope='module')
def login_inspector(test_client, new_inspector):
    test_client.post('/login_inspector', data=dict(email=new_inspector.email,password='12345678'))


@pytest.fixture(scope='module')
def create_report(test_client,login_reporter):
    Report.__table__.drop(db.engine)
    db.create_all()
    data=dict(first_name='John', last_name='Doe', sup_fname='Super', sup_lname='Visor', crew='1234', date='2020-03-01', cleanup='Moderate', building_type='Residential', city='San Diego', state='California', street_address='5500 Campanile Drive', zipcode=92182, notes='SDSU')

    response = test_client.post('/reporter/ccie', data=data)
    response = test_client.get('/reporter/sign_out')

@pytest.fixture(scope='module')
def drop_suspects():
    Suspect.__table__.drop(db.engine)
    db.create_all()