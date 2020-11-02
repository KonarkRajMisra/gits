from flask import render_template,request,Blueprint
from flask.helpers import url_for
from werkzeug.utils import redirect

core = Blueprint('core',__name__)

@core.route('/')
def index():
    return render_template('index.html')


@core.route('/signup')
def sign_up():
    return redirect(url_for('reporters_users.register_reporter'))