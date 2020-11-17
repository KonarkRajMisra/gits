from os import abort
from gitsapp.models import User
from gitsapp.inspectors.forms import RegistrationForm,LoginForm
from gitsapp import db, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user 
from flask import render_template, url_for, flash, redirect, request, Blueprint

#inspector flow
inspectors_users = Blueprint('inspectors_users', __name__)

#create inspector acc
@inspectors_users.route('/register_inspector',methods=['GET','POST'])
def register_inspector():
    form = RegistrationForm(request.form)
    
    if form.validate_on_submit():
        inspector = User(email=form.email.data,password=form.password.data, urole="LAW")
        db.session.add(inspector)
        db.session.commit()
       
        return redirect(url_for('inspectors_users.login_inspector'))
    return render_template('inspectors/register_inspector.html',form=form)


#login
@inspectors_users.route('/login_inspector',methods=['GET','POST'])
def login_inspector():
    if current_user.is_authenticated:
        if(current_user.urole == "LAW"):
            return redirect(url_for('inspectors_users.dash'))
        

        return redirect (url_for('reporters_users.dash'))
        

    form = LoginForm(request.form)
    if form.validate_on_submit():
        
        inspector = User.query.filter_by(email=form.email.data).first()
        
        if inspector and inspector.check_pwd(form.password.data):
            login_user(inspector)
            return redirect(url_for('inspectors_users.dash'))

        
    return render_template('inspectors/login_inspector.html',form=form)


#after login users should be directed to DASH
@inspectors_users.route('/inspector/dash', methods=['GET'])
@login_required(role="LAW")
def dash():
    return render_template('inspectors/inspector_dash.html', curr_user= current_user)

@inspectors_users.route('/inspector/sign_out')
@login_required(role="LAW")
def signout_inspector():
    logout_user()
    return redirect(url_for('core.index'))

@inspectors_users.route('/inspector/legi',methods=['GET','POST'])
@login_required
def legi_report():
    pass


#query all the reports created by the user, else give 403 unauth access
@inspectors_users.route('/reports',methods=['GET','POST'])
@login_required(role="LAW")
def reports(report_id):
    all_reports = Report.query.get_or_404(report_id)
    if all_reports.author != current_user:
        abort(403)
            
        