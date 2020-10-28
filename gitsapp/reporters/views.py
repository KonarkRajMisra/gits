from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from gitsapp import db
from werkzeug.security import generate_password_hash, check_password_hash
from gitsapp.models import Reporter, Report
from gitsapp.reporters.forms import RegistrationForm,LoginForm

reporters_users = Blueprint('users',__name__)

@reporters_users.route('/register_reporter',methods=['GET','POST'])
def register_reporter():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        reporter = Reporter(email=form.email.data,password=form.password.data)
        db.session.add(reporter)
        db.session.commit()
        
        return redirect(url_for('reporters_users.login'))
    return render_template('register_reporter.html',form=form)


@reporters_users.route('/login_reporter',methods=['GET','POST'])
def login_reporter():
    form = LoginForm()
    if form.validate_on_submit():
        
        reporter = Reporter.query.filter_by(email=form.email.data).first()
        
        if reporter.check_password(form.password.data) and reporter:
            login_user(reporter)
    return render_template('login_reporter.html',form=form)

#after login users should be directed to create a incident report
@reporters_users.route('/reporter_account',methods=['GET','POST'])
@login_required
def reporter_account():
    form = Report()
    
    #if form submitted create a report
    if form.validate_on_submit():
        pass
    
            
        