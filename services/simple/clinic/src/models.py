from db import db
import json

class Clinic(db.Model):
    __tablename__ = "clinic"
    clinicID = db.Column(db.String(36), primary_key=True)
    clinicName = db.Column(db.VARCHAR)
    location = db.Column(db.VARCHAR)
    services = db.Column(db.Text)  
    
    def __init__(self, clinicID, clinicName, location, services):
        self.clinicID = clinicID
        self.clinicName = clinicName
        self.location = location
        self.services = json.dumps(services)

    def json(self):
        return {
            "clinicID": self.clinicID,
            "clinicName": self.clinicName,
            "location": self.location,
            "services": json.loads(self.services),
        }