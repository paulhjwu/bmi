from app import db
from models.users import User

import math

class BMILOG(db.Document):
    meta = {'collection': 'bmilog'}
    user = db.ReferenceField(User)
    datetime = db.DateTimeField()
    weight = db.FloatField()
    height = db.FloatField()
    bmi = db.FloatField()
    
    def computeBMI(self, unit):
        if unit == 'm':
            bmi = self.weight / math.pow(self.height, 2)
        else:
            bmi = self.weight / math.pow(self.height/100, 2)
        return bmi