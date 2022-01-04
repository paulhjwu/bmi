# https://medium.com/@dmitryrastorguev/basic-user-authentication-login-for-flask-using-mongoengine-and-wtforms-922e64ef87fe

from app import app, db,login_manager
from flask import render_template, request
from flask_login import login_required, current_user

# Register Blueprint so we can factor routes
from auth import auth
from bmi import bmi, csv_to_dict, storeReadings
from dashboard import dashboard

# register blueprint from respective module
app.register_blueprint(auth)
app.register_blueprint(bmi)
app.register_blueprint(dashboard)

from users import User

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
        if type == 'create':
            print("No create Action yet")
        elif type == 'upload':
            file = request.files.get('file')
            listOfDict = csv_to_dict(file)
            storeReadings(listOfDict, db)
        return render_template("upload.html", name=current_user.name, panel="Upload")
    
