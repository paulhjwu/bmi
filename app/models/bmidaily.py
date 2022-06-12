from app import db
from models.users import User

# class Bmi_Measurement(db_Document):
class BMIDAILY(db.Document):
    
    meta = {'collection': 'bmidaily'}
    user = db.ReferenceField(User)
    date = db.DateTimeField()
    numberOfMeasures = db.IntField()
    averageBMI = db.FloatField()
    
    def updatedBMI(self, newBMI):
        return (newBMI + (self.averageBMI * self.numberOfMeasures)) / (self.numberOfMeasures + 1) 
