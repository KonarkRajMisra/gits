import os
from gitsapp.models import User,Report, Suspect
from gitsapp.inspectors.forms import RegistrationForm,LoginForm, LegiReportForm, SuspectForm, SearchSuspectForm
from gitsapp import db, login_required, app, gmap
from werkzeug.utils import secure_filename
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
        
        if inspector and inspector.check_pwd(form.password.data):
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
        pin_info = {
            "lat": report.gps_lat,
            "lng": report.gps_lng,
            #TODO Add link to LEGI form lnk: url_for('')

        }

        pins.append(pin_info)

    report_map = Map(identifier="reports_map", lat=39.8283, lng=-98.5795,marker=pins )
    
    
    

    return render_template('inspectors/inspector_dash.html', curr_user= current_user, pins=pins)

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
@inspectors_users.route('/inspector/legi/<int:report_id>/deletepic/<int:del_pic_id>', methods=['DELETE'])
@inspectors_users.route('/inspector/legi/<int:report_id>/editpic/<int:edit_pic_id>/<string:new_name>', methods=['POST'])
@login_required(role="LAW")
def legi_report(report_id, new_name=None, del_pic_id=None, edit_pic_id=None):
    
    legi_form = LegiReportForm()
    found = False
    search_form = SearchSuspectForm()
    sus_form = SuspectForm()
    
    report = Report.query.filter_by(id=report_id).first()
    suspect = None

    #If suspect is already attached
    if len(report.suspect) != 0:
        found = True
        suspect = report.suspect[0]


    #Delete a picture
    # if del_pic_id != None:
    #     os.remove(report.images[del_pic_id])
    #     report.images.remove(del_pic_id)
    #     db.session.commit()

    #Edit a picture
    # if edit_pic_id != None and new_name != None:
    #     img_path = report.images[edit_pic_id]
    #     new_path = os.path.join(os.path.dirname(img_path), new_name)

    #     os.rename(img_path, new_path)

    # if search_form.validate_on_submit():
    #     #Search suspect to autofill
    #     if search_form.first_name and search_form.last_name:
    #         for search_suspect in Suspect.query.all():
    #             if search_suspect.first_name == search_form.first_name and suspect.last_name == search_form.last_name:
    #                 suspect = search_suspect
    #                 found = True
        
    #     found = False



    if sus_form.validate_on_submit():
        suspect = Suspect(sus_form.first_name.data, sus_form.last_name.data, sus_form.gang.data, sus_form.status.data if sus_form.status.data != "No Change" else "Unknown")

        report.suspect = [suspect]

        # directory = os.path.join(app.instance_path, 'sus_photos')
        db.session.add(suspect)
        db.session.commit()
        found=True
        # for image in sus_form.sus_photos.data:
        #     filename=secure_filename(image.filename)
        

        #     file_path = os.path.join(directory, filename)
        #     image.save(file_path)
        #     suspect.images.append(file_path)
    

    
    elif legi_form.validate_on_submit():
        #Find GPS coordinates
        result = gmap.geocode(legi_form.street_address.data)
        #basic check to make sure address matches state
        try:
            report.gps_lat = result[0].get("geometry").get("location").get("lat")
            report.gps_lng = result[0].get("geometry").get("location").get("lng")        
        except:
            legi_form.street_address.errors.append('Invalid Address')
            return render_template('inspectors/LEGI_report.html',report=report, suspect=suspect, sus_form=sus_form, legi_form=legi_form, search_form=search_form, found=found)
        report.street_address = legi_form.street_address.data
        report.zipcode = legi_form.zipcode.data
        report.moniker = legi_form.moniker.data
        report.cross_street = legi_form.cross_street.data
        
        if legi_form.building_type.data != "No Change": 
            report.building_type = legi_form.building_type.data

        if legi_form.investigation_status.data != "No Change":
            report.investigation_status = legi_form.investigation_status.data

        if legi_form.cleanup.data != "No Change":    
            report.scale_of_cleanup = legi_form.cleanup.data

        #Adding images
        # directory = os.path.join(app.instance_path, 'report_photos')
        # if not os.path.exists(directory):
        #     os.makedirs(directory)

        # for image in legi_form.new_photos.data:
        #     filename=secure_filename(image.filename)
          

        #     file_path = os.path.join(directory, filename)
        #     image.save(file_path)
        #     report.images.append(file_path)
            
        db.session.commit()

    return render_template('inspectors/LEGI_report.html',report=report, suspect=suspect, sus_form=sus_form, legi_form=legi_form, search_form=search_form, found=found)



            