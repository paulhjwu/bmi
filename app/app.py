# https://medium.com/@dmitryrastorguev/basic-user-authentication-login-for-flask-using-mongoengine-and-wtforms-922e64ef87fe

from flask_login import login_required, current_user
from flask import render_template, request
from app import app, db, login_manager

# Register Blueprint so we can factor routes
# from bmi import bmi, get_dict_from_csv, insert_reading_data_into_database
from bmi import bmi
from dashboard import dashboard, CHART
from auth import auth

# register blueprint from respective module
app.register_blueprint(dashboard)
app.register_blueprint(auth)
app.register_blueprint(bmi)

from users import User
from dashboard import CHART
from bmi import BMIDAILY
import csv
import io

# Load the current user if any
@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()

@app.route('/base')
def show_base():
    return render_template('base.html')

@app.route('/log')
def log():
    return render_template('log.html', name=current_user.name, panel="Logging BMI")
 
@app.route("/upload", methods=['GET','POST'])
@login_required
def upload():
    
    if request.method == 'GET':
        return render_template("upload.html", name=current_user.name, panel="Upload")
    elif request.method == 'POST':
        
        type = request.form.get('type')
        file = request.files.get('file')                    
        data = file.read().decode('utf-8')
        dict_reader = csv.DictReader(io.StringIO(data), delimiter=',', quotechar='"')
        file.close()
        
        if type == 'create':
            print("No create Action yet")
        elif type == 'upload':
            
            for item in list(dict_reader):
                existing_user = User.objects(email=item['User_email']).first()
                if existing_user:
                    measure_date=item['Date']
                    num_of_measure=item['Num']
                    bmi=item['BMI']
                    a_bmidaily = BMIDAILY(user=existing_user, date=measure_date, 
                            numberOfMeasures=num_of_measure, averageBMI=bmi).save()
        
        return render_template("upload.html", name=current_user.name, panel="Upload")
