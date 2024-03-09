from db import db
import json

class Patient(db.Model):
    __tablename__ = "patient"
    patientID = db.Column(db.String(36), primary_key=True)
    patientName = db.Column(db.VARCHAR)
    contactNum = db.Column(db.Integer)
    allergies = db.Column(db.Text)
    medications = db.Column(db.Text)

    def __init__(self, patientID, patientName, contactNum, allergies, medications):
        self.patientID = patientID
        self.patientName = patientName
        self.contactNum = contactNum
        self.allergies = json.dumps(allergies)
        self.medications = json.dumps(medications)

    def json(self):
        return {
            "patientID": self.patientID,
            "patientName": self.patientName,
            "contactNum": self.contactNum,
            "allergies": json.loads(self.allergies),
            "medications": json.loads(self.medications),
        }

class Doctor(db.Model):
    __tablename__ = 'doctor'
    doctorID = db.Column(db.String(36), primary_key=True)
    clinicID = db.Column(db.String(36))
    doctorName = db.Column(db.VARCHAR)
    doctorDesc = db.Column(db.VARCHAR(255))
    specialty = db.Column(db.VARCHAR)
    ratings = db.Column(db.Float)

    def __init__(self, clinicID, doctorID, doctorName, doctorDesc, specialty, ratings):
        self.clinicID = clinicID
        self.doctorID = doctorID
        self.doctorName = doctorName
        self.doctorDesc = doctorDesc
        self.specialty = specialty
        self.ratings = ratings

    def json(self):
        return {
            "clinicID": self.clinicID,
            "doctorID": self.doctorID,
            "doctorName": self.doctorName,
            "doctorDesc": self.doctorDesc,
            "specialty": self.specialty,
            "ratings": self.ratings
        }