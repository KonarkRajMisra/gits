from os import abort
from gitsapp.models import Inspector
from gitsapp.inspectors.forms import RegistrationForm,LoginForm
from gitsapp import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user, login_required
from flask import render_template, url_for, flash, redirect, request, Blueprint

#inspector flow
inspectors_users = Blueprint('inspector_users', __name__)

#create inspector acc
@inspectors_users.route('/register_inspector',methods=['GET','POST'])
def register_inspector():
    form = RegistrationForm(request.form)
    
    if form.validate_on_submit():
        inspector = Inspector(email=form.email.data,password=form.password.data)
        db.session.add(inspector)
        db.session.commit()
       
        return redirect(url_for('inspectors_users.login_inspector'))

    print(form.errors)
    return render_template('inspectors/register_inspector.html',form=form)


#login
@inspectors_users.route('/login_inspector',methods=['GET','POST'])
def login_inspector():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        
        inspector = Inspector.query.filter_by(email=form.email.data).first()
        
        if inspector.check_password(form.password.data) and inspector:
            login_user(inspector)

        return redirect(url_for('inspectors_users.dash'))
    return render_template('inspectors/login_inspector.html',form=form)


#after login users should be directed to DASH
@inspectors_users.route('/inspector/dash', methods=['GET'])
@login_required
def dash():
    return render_template('inspectors/inspector_dash.html')


@inspectors_users.route('/inspector/legi',methods=['GET','POST'])
@login_required
def legi_report():
    pass


#query all the reports created by the user, else give 403 unauth access
@inspectors_users.route('/reports',methods=['GET','POST'])
@login_required
def reports(report_id):
    all_reports = Report.query.get_or_404(report_id)
    if all_reports.author != current_user:
        abort(403)
            
        