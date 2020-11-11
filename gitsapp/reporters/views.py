from os import abort
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from gitsapp import db
from werkzeug.security import generate_password_hash, check_password_hash
from gitsapp.models import Reporter, Report
from gitsapp.reporters.forms import RegistrationForm,LoginForm, CCIEReportForm

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
        
        if reporter.check_pwd(form.password.data) and reporter is not None:
            login_user(reporter)
            next = request.args.get('next')
            flash('logged in')
            if next:
                return redirect(next)
            
            return redirect(url_for('reporters_users.reporter_account'))
    return render_template('login_reporter.html',form=form)


#after login users should be directed to create a incident report
@reporters_users.route('/reporter_account',methods=['GET','POST'])
@login_required
def reporter_account():
    
    form = CCIEReportForm()
    #if form submitted create a report
    print(form.validate_on_submit())
    if form.validate_on_submit():
        print("validated")
        report = Report(supervisor_fname=form.first_name.data,
                        supervisor_lname=form.last_name.data,
                        crew_id=form.crew.data,
                        date_of_incident=form.date.data,
                        type_of_building=form.building_type.data,
                        street_address=form.street_address.data,
                        zipcode=form.zipcode.data,
                        notes=form.notes.data,author_id=current_user.id)
        db.session.add(report)
        db.session.commit()
    # elif not form.validate_on_submit():
    #     print(form.errors)
        return redirect(url_for('reporters_users.reports',report_id=report.id))
    
    #otherwise show the form
    return render_template('create_report.html',form=form)



#query all the reports created by the user, else give 403 unauth access
@reporters_users.route('/<int:report_id>',methods=['GET','POST'])
@login_required
def reports(report_id):
    report = Report.query.get_or_404(report_id)
    return render_template('reports.html',report=report)
            
        