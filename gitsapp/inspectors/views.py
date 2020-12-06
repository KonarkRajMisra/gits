from os import abort
from gitsapp.models import User,Report
from gitsapp.inspectors.forms import RegistrationForm,LoginForm
from gitsapp import db, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user 
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_googlemaps import Map
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
        

    form = LoginForm(request.form)
    if form.validate_on_submit():
        
        inspector = User.query.filter_by(email=form.email.data).first()

        if(inspector.urole == "WORKER"):
            form.email.errors.append("This is a City Worker account. Use the City Worker login to use this account")
        
        elif inspector and inspector.check_pwd(form.password.data):
            login_user(inspector)
            return redirect(url_for('inspectors_users.dash'))

        
    return render_template('inspectors/login_inspector.html',form=form)


#after login users should be directed to DASH
@inspectors_users.route('/inspector/dash', methods=['GET'])
@login_required(role="LAW")
def dash():

    reports = Report.query.all()
    pins = [];

    for report in reports:
        #TODO add this code onto Graffiti Analysis for hotspots 
        if report.is_hotspot:
            pin_info = {
                'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
                "lat": report.gps_lat,
                "lng": report.gps_lng,
                "infobox": 
                '<a href="' + url_for('inspectors_users.legi_report', report_id=report.id) + '">LEGI Report</a> <form method="POST" id="hotspot"><a href="' + url_for('inspectors_users.toggle_hotspot', report_id = report.id) + '"' + "onclick=\"document.getElementById('hotspot').submit();\">Remove hotspot</a></form>"
            }

        else:
             pin_info = {
                 'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
                "lat": report.gps_lat,
                "lng": report.gps_lng,
                "infobox": 
                '<a href="' + url_for('inspectors_users.legi_report', report_id=report.id) + '">LEGI Report</a> <form method="POST" id="hotspot"><a href="' + url_for('inspectors_users.toggle_hotspot', report_id = report.id) + '"' + "onclick=\"document.getElementById('hotspot').submit();\">Make hotspot</a></form>"
            }
        pins.append(pin_info)

    report_map = Map(identifier="reports_map", lat=39.8283, lng=-98.5795,marker=pins )
    

    return render_template('inspectors/inspector_dash.html', curr_user= current_user, pins=pins)

@inspectors_users.route('/inspector/togglespot/<int:report_id>', methods=['GET','POST'])
def toggle_hotspot(report_id):
    report = Report.query.filter(Report.id == report_id)[0]
    report.is_hotspot = not report.is_hotspot
    db.session.commit()
    return redirect(url_for('inspectors_users.dash'))

@inspectors_users.route('/inspector/sign_out')
@login_required(role="LAW")
def signout_inspector():
    logout_user()
    return redirect(url_for('core.index'))

#query all the reports created by the user, else give 403 unauth access
# @inspectors_users.route('/reports',methods=['GET','POST'])
# @login_required(role="LAW")
# def reports(report_id):
#     all_reports = Report.query.get_or_404(report_id)
#     if all_reports.author != current_user:
#         abort(403)
            

@inspectors_users.route('/inspector/gr/', methods=['GET'])
@inspectors_users.route('/inspector/gr/<string:data>', methods=['GET'])
@login_required(role="LAW")
def graffiti_reporting(data=None):

    urls = []
    reports = []

    if data != None:
        
        for report in Report.query.all():
            if report.has_keyword(data):
                urls.append(url_for('inspectors_users.legi_report',report_id=report.id))
                reports.append(report)



    return render_template('inspectors/graffiti_reporting.html',report_links=urls, report_objs=reports)        





         
@inspectors_users.route('/inspector/all_reports',methods=['GET'])
@login_required(role="LAW")
def all_reports():
    reports = Report.query.order_by(Report.id).all()
    return render_template('inspectors/all_reports.html',reports=reports)

@inspectors_users.route('/inspector/legi/<int:report_id>',methods=['GET','POST'])
@login_required(role="LAW")
def legi_report(report_id):
    report = Report.query.filter_by(id=report_id).first()
    return render_template('inspectors/LEGI_report.html',report=report)



            
