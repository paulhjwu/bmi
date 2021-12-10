# https://medium.com/@dmitryrastorguev/basic-user-authentication-login-for-flask-using-mongoengine-and-wtforms-922e64ef87fe
import math

from app import app, db, dbd, login_manager

# from flask import Flask, Blueprint, render_template, request, redirect, url_for
from flask import Blueprint, render_template, request, jsonify

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

# Initialize the App
#app, db, login_manager = create_app()

# Register Blueprint so we can factor routes

from auth import auth
from bmi import bmi, csv_to_dict, storeReadings
from dashboard import dashboard

app.register_blueprint(auth)
app.register_blueprint(bmi)
app.register_blueprint(dashboard)

from users import User

# For flask-login

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
        #render_template("upload.html")
    elif request.method == 'POST':
        type = request.form.get('type')
        if type == 'create':
            print("No create Action yet")
        elif type == 'upload':
            file = request.files.get('file')
            # upload_logs(file)
            listOfDict = csv_to_dict(file)
            storeReadings(listOfDict, db)
        return render_template("upload.html", name=current_user.name, panel="Upload")
    
