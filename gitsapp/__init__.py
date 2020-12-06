#configuration files
#configuration files
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_googlemaps import GoogleMaps
from flask_login import LoginManager, current_user
from functools import wraps
import googlemaps



app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

#Configurations
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['GOOGLEMAPS_KEY'] = "AIzaSyD7IJ8NOPPuyGymr2fStLpV-TJfda1JRsY"
app.config['STATIC'] = os.path.join(app.root_path, 'static')

GoogleMaps(app)
gmap = googlemaps.Client(key=app.config['GOOGLEMAPS_KEY'])


#db setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

#Login Manager Configs
login_manager = LoginManager()
login_manager.init_app(app)

def login_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
               return app.login_manager.unauthorized()
            urole = current_user.urole
            if ( (urole != role) and (role != "ANY")):
                return app.login_manager.unauthorized()      
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

#TODO: Create users.login view in /gitsapp/ussers

login_manager.login_view = 'core.index'

#TODO: Blueprint configs
from gitsapp.core.views import core
from gitsapp.reporters.views import reporters_users
from gitsapp.inspectors.views import inspectors_users 

app.register_blueprint(core)
app.register_blueprint(reporters_users)
app.register_blueprint(inspectors_users)