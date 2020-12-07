import os
from gitsapp.models import User,Report, Suspect, Suspect_Image, Report_Image
from gitsapp.inspectors.forms import RegistrationForm,LoginForm, LegiReportForm, SuspectForm, SearchSuspectForm, SearchForm, GraffitiAnalysisForm
from gitsapp import db, login_required, app, gmap
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user 
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_googlemaps import Map
from collections import Counter
from datetime import date
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

        if(inspector == None or inspector.urole == "WORKER"):
            form.email.errors.append("This is a City Worker account. Use the City Worker login to use this account")
            return render_template('inspectors/login_inspector.html',form=form)
        
        elif inspector and inspector.check_pwd(form.password.data):
            login_user(inspector)
            return redirect(url_for('inspectors_users.dash'))

        
    return render_template('inspectors/login_inspector.html',form=form)


#after login users should be directed to DASH
@inspectors_users.route('/inspector/dash', methods=['GET'])
@login_required(role="LAW")
def dash():
    reports = Report.query.all()
    pins = []

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
        

         
@inspectors_users.route('/inspector/all_reports',methods=['GET'])
@login_required(role="LAW")
def all_reports():
    reports = Report.query.order_by(Report.id).all()
    return render_template('inspectors/all_reports.html',reports=reports)


@inspectors_users.route('/inspector/legi/<int:report_id>',methods=['GET','POST'])
@login_required(role="LAW")
def legi_report(report_id, new_name=None, del_pic_id=None, edit_pic_id=None):
    
    legi_form = LegiReportForm()
    found = None
    search_form = SearchSuspectForm()
    sus_form = SuspectForm()
    
    report = Report.query.filter_by(id=report_id).first()
    suspect = None
    status=None
    #If suspect is already attached
    if len(report.suspect) != 0:
        found = True
        suspect = report.suspect[0]

    if search_form.validate_on_submit() and suspect == None:
        #Search suspect to autofill
        if search_form.search_first_name.data and search_form.search_last_name.data:
            for search_suspect in Suspect.query.all():
                if search_suspect.first_name == search_form.search_first_name.data and search_suspect.search_last_name == search_form.search_last_name.data:
                    suspect = search_suspect
                    found = True
                    report.suspect.append(suspect)
                    db.session.commit()
                    break
            
            if suspect == None:
                suspect = Suspect(search_form.search_first_name.data, search_form.search_last_name.data)
                db.session.add(suspect)
                db.session.commit()
                report.suspect.append(suspect)
                db.session.commit()
                found=False
                status=404


    elif sus_form.validate_on_submit():
        directory = os.path.join(app.config['STATIC'], 'sus_photos')
        if not os.path.exists(directory):
            os.makedirs(directory)

        suspect.first_name = sus_form.first_name.data if sus_form.first_name.data != None else suspect.first_name

        suspect.last_name = sus_form.last_name.data if sus_form.last_name != None else suspect.last_name

        suspect.gang = sus_form.gang.data if sus_form.gang.data != None else suspect.gang

        suspect.status = sus_form.status.data if sus_form.status.data != "No Change" else suspect.status

        db.session.commit()

        try:
            for image in sus_form.sus_photos.data:
                filename=secure_filename(image.filename)
                file_path = os.path.join(directory, filename)
                image.save(file_path)
                sus_image = Suspect_Image(file_path, suspect.id, filename)
                db.session.add(sus_image)
                db.session.commit()
                suspect.images.append(sus_image)
                db.session.commit()
        
        except:
            pass
      
    elif legi_form.validate_on_submit():
        #Find GPS coordinates
        result = gmap.geocode(legi_form.street_address.data)
        #basic check to make sure address matches state
        try:
            report.gps_lat = result[0].get("geometry").get("location").get("lat")
            report.gps_lng = result[0].get("geometry").get("location").get("lng")        
        except:
            legi_form.street_address.errors.append('Invalid Address')
            return render_template('inspectors/LEGI_report.html',report=report, suspect=suspect, sus_form=sus_form, legi_form=legi_form, search_form=search_form, found=found, image_list=report.images)
        report.street_address = legi_form.street_address.data
        report.zipcode = legi_form.zipcode.data
        report.moniker = legi_form.moniker.data
        report.cross_street = legi_form.cross_street.data
        
        if legi_form.type_of_building.data != "No Change": 
            report.type_of_building = legi_form.type_of_building.data

        if legi_form.investigation_status.data != "No Change":
            report.investigation_status = legi_form.investigation_status.data

        if legi_form.cleanup.data != "No Change":    
            report.scale_of_cleanup = legi_form.cleanup.data

        db.session.commit()
        #Adding images
        try:
            directory = os.path.join(app.config['STATIC'], 'report_photos')
            if not os.path.exists(directory):
                os.makedirs(directory)

            for image in legi_form.new_photos.data:
                filename=secure_filename(image.filename)

                file_path = os.path.join(directory, filename)
                image.save(file_path)
                rep_image = Report_Image(file_path, report.id, filename)
                db.session.add(rep_image)
                db.session.commit()
                report.images.append(rep_image)
                db.session.commit()
        except:
            return redirect(url_for('inspectors_users.all_reports'))
        return redirect(url_for('inspectors_users.all_reports'))

    return render_template('inspectors/LEGI_report.html',report=report, suspect=suspect, sus_form=sus_form, legi_form=legi_form, search_form=search_form, found=found, image_list=report.images, sus_image_list= suspect.images if suspect != None else None), status

@inspectors_users.route('/inspector/graffiti_analysis', methods=['GET','POST'])
@login_required(role="LAW")
def graffiti_analysis():

    form = GraffitiAnalysisForm()
    pins = []

    if form.validate_on_submit():
        reports = Report.query.all()
        for report in reports:
            
            if form.start_date.data == str(report.date_of_incident).split(" ")[0] or form.end_date.data == str(report.date_of_incident).split(" ")[0] or form.start_gps_lat.data == report.gps_lat or form.start_gps_lng.data == report.gps_lng or form.end_gps_lng.data == report.gps_lat or form.end_gps_lat.data == report.gps_lat or form.suspect_name.data == report.first_name + report.last_name:
                pin_info = {
                    'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
                    "lat": report.gps_lat,
                    "lng": report.gps_lng,
                    "infobox": 
                    '<a href="' + url_for('inspectors_users.legi_report', report_id=report.id) + '">LEGI Report</a> <form method="POST" id="hotspot"><a href="' + url_for('inspectors_users.toggle_hotspot', report_id = report.id) + '"' + "onclick=\"document.getElementById('hotspot').submit();\">Remove hotspot</a></form>"
                }
                pins.append(pin_info)

    report_map = Map(identifier="reports_map", lat=39.8283, lng=-98.5795,marker=pins )

    return render_template('inspectors/graffitianalysis.html',form=form,pins=pins)




@inspectors_users.route('/inspector/gr/', methods=['GET','POST'])
@login_required(role="LAW")
def graffiti_reporting(data=None):

    form = SearchForm()
    urls = []
    reports = []

    if form.validate_on_submit():

        for report in Report.query.all():
            if report.has_keyword(form.search.data):
                urls.append(url_for('inspectors_users.legi_report',report_id=report.id))
                reports.append(report)

    
    return render_template('inspectors/graffiti_reporting.html',links=urls, reports=reports,form=form)

@inspectors_users.route('/inspector/status_report')
@login_required(role="LAW")
def status_report():
    reports = Report.query.order_by(Report.id).all()
    law_enforcers = User.query.filter_by(urole="LAW")
    new_incident = 0
    if law_enforcers:
        total_law = []
        for officer in law_enforcers:
            total_law.append(officer)
    total_law = len(total_law)
    total_incidents = len(reports)
    today = date.today()
    reports = Report.query.all()
    suspects = Suspect.query.all()
    incidents_with_no_suspects = len(reports) - len(suspects)
    incidents_with_identified_suspects = Suspect.query.filter_by(status="Identified").count()
    incidents_with_suspects_in_custody = Suspect.query.filter_by(status="In Custody").count()
    incidents_with_suspects_released = Suspect.query.filter_by(status="Released").count()
    incidents_resolved = Report.query.filter_by(investigation_status="Resolved").count()
    


    return render_template('inspectors/status_report.html',today=today,total_law=total_law, new_incident=new_incident, total_incidents=total_incidents,incidents_with_no_suspects=incidents_with_no_suspects,incidents_with_identified_suspects=incidents_with_identified_suspects,incidents_with_suspects_in_custody =incidents_with_suspects_in_custody ,incidents_with_suspects_released=incidents_with_suspects_released,incidents_resolved=incidents_resolved)