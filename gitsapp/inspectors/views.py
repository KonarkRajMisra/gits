from os import abort
from gitsapp.models import User,Report, Suspect
from gitsapp.inspectors.forms import RegistrationForm,LoginForm, LegiReportForm, SuspectForm
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
def legi_report(report_id, new_name, del_pic_id=None, edit_pic_id=None):
    sus_form = SuspectForm()
    legi_form = LegiReportForm()
    report = Report.query.filter_by(id=report_id).first()
    suspect = None

    #Delete a picture
    if del_pic_id != None:
        os.remove(report.images[del_pic_id])
        report.images.remove(del_pic_id)
        db.session.commit()
        return render_template('inspectors/LEGI_report.html',report=report)

    #Edit a picture
    if edit_pic_id != None and new_name != None:
        img_path = report.images[edit_pic_id]
        new_path = os.path.join(os.path.dirname(img_path), new_name)

        os.rename(img_path, new_path)
        return render_template('inspectors/LEGI_report.html',report=report)

    if sus_form.validate_on_submit() and not legi_form.validate_on_submit():
        #Search suspect to autofill
        if sus_form.first_name and sus_form.last_name:
            suspect = Suspect.query.filter(Suspect.first_name.like(sus_form.first_name)).filter(Suspect.last_name.like(sus_form.last_name))[0]
            report.suspect = suspect
        
        else:
            sus_form.errors.first_name.append("Suspect does not exist. Continue adding information")


    
    if legi_form.validate_on_submit() and sus_form.validate_on_submit():
        
        #Find GPS coordinates
        result = gmap.geocode(legi_form.street_address.data)
        #basic check to make sure address matches state
        if(result[0].get("address_components")[5].get("long_name") != report.state):
            legi_form.errors.append('Invalid state')
            return render_tempalte('Reporters/CCIE_report.html', legi_form=legi_form)

        report.gps_lat = result[0].get("geometry").get("location").get("lat"),
        report.gps_lng = result[0].get("geometry").get("location").get("lng"),
        report.street_address = legi_form.street_address
        report.building_type = legi_form.building_type
        report.zipcode = legi_form.zipcode
        report.moniker = legi_form.moniker
        report.cross_street = legi_form.cross_street
        report.investigation_status = legi_form.investigation_status
        report.cleanup = legi_form.cleanup


        #In case suspect does not exist
        if suspect == None:
            suspect = Suspect(sus_form.first_name, sus_form.last_name, sus_form.gang, sus_form.status)
            directory = os.path.join(app.instance_path, 'sus_photos')
            for image in form.sus_photos.data:
                filename=secure_filename(image.filename)
            

                file_path = os.path.join(directory, filename)
                image.save(file_path)
                suspect.images.append(file_path)


        #Adding images
        directory = os.path.join(app.instance_path, 'report_photos')
        if not os.path.exists(directory):
            os.makedirs(directory)

        for image in form.new_photos.data:
            filename=secure_filename(image.filename)
          

            file_path = os.path.join(directory, filename)
            image.save(file_path)
            report.images.append(file_path)
            
        db.commit()
    return render_template('inspectors/LEGI_report.html',report=report, suspect=suspect)



            