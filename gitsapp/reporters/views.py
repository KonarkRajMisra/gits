from os import abort
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from gitsapp import db
from werkzeug.security import generate_password_hash, check_password_hash
from gitsapp.models import Reporter, Report
from gitsapp.reporters.forms import RegistrationForm,LoginForm, ReportForm

#reporter flow
reporters_users = Blueprint('reporters_users',__name__)

#create reporter acc
@reporters_users.route('/register_reporter',methods=['GET','POST'])
def register_reporter():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        reporter = Reporter(email=form.email.data,password=form.password.data)
        db.session.add(reporter)
        db.session.commit()
        
        return redirect(url_for('reporters_users.login_reporter'))
    return render_template('register_reporter.html',form=form)


#login
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
    form = ReportForm()
    
    #if form submitted create a report
    if form.validate_on_submit():
        report = Report(form.first_name.data,form.last_name.data,form.crew.data,form.date.data,form.building_type.data,form.street_address.data,form.zipcode.data,form.notes.data)
        db.session.add(report)
        db.session.commit()
        
        #redirect to reports page
        return redirect(url_for(reporters_users.reports))
    #otherwise show the form
    return render_template('create_report.html',form=form)


#query all the reports created by the user, else give 403 unauth access
@reporters_users.route('/reports',methods=['GET','POST'])
@login_required
def reports(report_id):
    all_reports = Report.query.get_or_404(report_id)
    if all_reports.author != current_user:
        abort(403)
            
        