from app import db
from flask_login import UserMixin
class User(UserMixin, db.Document):
    meta = {'collection': 'appUsers'}
    email = db.StringField(max_length=30)
    password = db.StringField()
    name = db.StringField()
