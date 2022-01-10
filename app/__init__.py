from flask import Flask
from flask_mongoengine import MongoEngine, Document
from flask_login import LoginManager

import pymongo

def create_app():
    app = Flask(__name__)
    app.config['MONGODB_SETTINGS'] = {
        'db':'db_name',
        'host':'localhost'
    }
    app.static_folder = 'assets'
    db = MongoEngine(app)

    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    return app, db, login_manager

app, db, login_manager = create_app()

