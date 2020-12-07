from gitsapp.models import User, db
from gitsapp.reporters.forms import RegistrationForm
from gitsapp import app
import pytest

@pytest.fixture(scope='module')
def new_reporter():
    db.drop_all()
    db.create_all()
    user = User('reporter@test.com', '12345678', 'WORKER')
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture(scope='module')
def new_inspector():
    db.drop_all()
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