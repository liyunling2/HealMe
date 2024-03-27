from db import db
import uuid
from datetime import datetime
from sqlalchemy.sql import func

# class ClinicRating(db.Model):
#     __tablename__ = 'clinic_rating'
    
#     ratingID = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
#     clinicID = db.Column(db.String(36))
#     patientID = db.Column(db.String(36))
#     timeStamp = db.Column(db.DateTime, default=func.now(), onupdate=func.now())
#     ratingGiven = db.Column(db.Float)
#     comments = db.Column(db.VARCHAR(255))

#     def __init__(self, ratingID, clinicID, patientID, ratingGiven, comments):
#         self.ratingID = ratingID
#         self.clinicID = clinicID
#         self.patientID = patientID
#         self.ratingGiven = ratingGiven
#         self.comments = comments

#     __table_args__ = (db.UniqueConstraint('ratingID', 'clinicID', 'patientID', name='unique_clinic_rating'),)

#     def json(self):
#         return {
#             "ratingID": self.ratingID,
#             "clinicID": self.clinicID,
#             "patientID": self.patientID,
#             "timeStamp": self.timeStamp,
#             "ratingGiven": self.ratingGiven,
#             "comments": self.comments,
#         }
    
class DoctorRating(db.Model):
    __tablename__ = 'doctor_rating'
    
    ratingID = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    clinicID = db.Column(db.String(36))
    doctorID = db.Column(db.String(36))
    appointmentID = db.Column(db.String(36))
    patientID = db.Column(db.String(36))
    timeStamp = db.Column(db.DateTime, default=func.now(), onupdate=func.now())
    ratingGiven = db.Column(db.Float)
    comments = db.Column(db.VARCHAR(255))

    def __init__(self, ratingID, clinicID, doctorID, appointmentID, patientID, ratingGiven, comments):
        self.ratingID = ratingID
        self.clinicID = clinicID
        self.doctorID = doctorID
        self.appointmentID = appointmentID
        self.patientID = patientID
        self.ratingGiven = ratingGiven
        self.comments = comments

    __table_args__ = (db.UniqueConstraint('ratingID', 'clinicID', 'doctorID', 'appointmentID', 'patientID', name='unique_doctor_rating'),)

    def json(self):
        return {
            "ratingID": self.ratingID,
            "clinicID": self.clinicID,
            "doctorID": self.doctorID,
            "appointmentID": self.appointmentID,
            "patientID": self.patientID,
            "timeStamp": self.timeStamp,
            "ratingGiven": self.ratingGiven,
            "comments": self.comments,
        }