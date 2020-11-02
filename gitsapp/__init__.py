#configuration files
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)

#Configurations
app.config['SECRET_KEY'] = 'mysecretkey'

#db setup
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

#Login Manager Configs
login_manager = LoginManager()
login_manager.init_app(app)

#TODO: Create users.login view in /gitsapp/ussers
login_manager.login_view = 'reporters_users.login'

#TODO: Blueprint configs
from gitsapp.core.views import core
from gitsapp.reporters.views import reporters_users

app.register_blueprint(core)
app.register_blueprint(reporters_users)