from db import db
import json
import uuid

class Patient(db.Model):
    __tablename__ = "patient"
    patientID = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.VARCHAR(255), unique=True)
    password = db.Column(db.VARCHAR(255))
    patientName = db.Column(db.VARCHAR(255))
    contactNum = db.Column(db.Integer, unique=True)
    # allergies = db.Column(db.Text)
    # medications = db.Column(db.Text)

    def __init__(self, patientID, email, password, patientName, contactNum):
        self.patientID = patientID
        self.email = email
        self.password = password
        self.patientName = patientName
        self.contactNum = contactNum
        # self.allergies = json.dumps(allergies)
        # self.medications = json.dumps(medications)

    __table_args__ = (db.UniqueConstraint('patientID', 'contactNum', 'email', name='unique_patient'),)

    def json(self):
        return {
            "patientID": self.patientID,
            "email": self.email,
            "password": self.password,
            "patientName": self.patientName,
            "contactNum": self.contactNum,
            # "allergies": json.loads(self.allergies),
            # "medications": json.loads(self.medications),
        }

class Doctor(db.Model):
    __tablename__ = 'doctor'
    doctorID = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    clinicID = db.Column(db.String(36))
    email = db.Column(db.VARCHAR(255), unique=True)
    password = db.Column(db.VARCHAR(255))
    doctorName = db.Column(db.VARCHAR(255))
    doctorDesc = db.Column(db.VARCHAR(255))
    specialty = db.Column(db.VARCHAR(255))

    def __init__(self, doctorID, clinicID, email, password, doctorName, doctorDesc, specialty):
        self.doctorID = doctorID
        self.clinicID = clinicID
        self.email = email
        self.password = password
        self.doctorName = doctorName
        self.doctorDesc = doctorDesc
        self.specialty = specialty

    __table_args__ = (db.UniqueConstraint('doctorID', 'email', name='unique_doctor'),)

    def json(self):
        return {
            "clinicID": self.clinicID,
            "email": self.email,
            "password": self.password,
            "doctorID": self.doctorID,
            "doctorName": self.doctorName,
            "doctorDesc": self.doctorDesc,
            "specialty": self.specialty,
        }