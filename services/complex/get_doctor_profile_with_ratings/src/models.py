from db import db
import json
import uuid

class Doctor(db.Model):
    __tablename__ = 'doctor'
    doctorID = db.Column(db.String(36), primary_key=True)
    clinicID = db.Column(db.String(36))
    doctorName = db.Column(db.VARCHAR(255))
    doctorDesc = db.Column(db.VARCHAR(255))
    specialty = db.Column(db.VARCHAR(255))

    def json(self):
        return {
            "clinicID": self.clinicID,
            "password": self.password,
            "doctorID": self.doctorID,
            "doctorName": self.doctorName,
            "doctorDesc": self.doctorDesc,
            "specialty": self.specialty,
            "ratings": self.ratings
        }

class DoctorRating(db.Model):
    __tablename__ = 'doctor_rating'
    ratingID = db.Column(db.String(36), primary_key=True)
    clinicID = db.Column(db.String(36))
    doctorID = db.Column(db.String(36), db.ForeignKey('doctor.doctorID'))
    appointmentID = db.Column(db.String(36))
    patientID = db.Column(db.String(36))
    timeStamp = db.Column(db.DateTime)
    ratingGiven = db.Column(db.Float)
    comments = db.Column(db.VARCHAR(255))

    def json(self):
        return {
            "ratingID": self.ratingID,
            "clinicID": self.clinicID,
            "doctorID": self.doctorID,
            "appointmentID": self.appointmentID,
            "patientID": self.patientID,
            "timeStamp": self.timeStamp.strftime("%Y-%m-%d %H:%M:%S"),
            "ratingGiven": self.ratingGiven,
            "comments": self.comments
        }