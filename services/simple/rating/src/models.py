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
    doctorName = db.Column(db.VARCHAR(255))
    bookingID = db.Column(db.String(36))
    clinicName = db.Column(db.VARCHAR(255))
    patientID = db.Column(db.String(36))
    patientName = db.Column(db.VARCHAR(255))
    bookingDate = db.Column(db.DateTime)
    timeStamp = db.Column(db.DateTime, default=func.now(), onupdate=func.now())
    ratingGiven = db.Column(db.Float)
    comments = db.Column(db.VARCHAR(255))

    def __init__(self, ratingID, clinicID, doctorID, doctorName, bookingID, clinicName, patientID, patientName, bookingDate, ratingGiven, comments):
        self.ratingID = ratingID
        self.clinicID = clinicID
        self.doctorID = doctorID
        self.doctorName = doctorName
        self.bookingID = bookingID
        self.clinicName = clinicName
        self.patientID = patientID
        self.patientName = patientName
        self.bookingDate = bookingDate
        self.ratingGiven = ratingGiven
        self.comments = comments

    __table_args__ = (db.UniqueConstraint('ratingID', 'clinicID', 'doctorID', 'bookingID', 'patientID', name='unique_doctor_rating'),)

    def json(self):
        return {
            "ratingID": self.ratingID,
            "clinicID": self.clinicID,
            "doctorID": self.doctorID,
            "doctorName": self.doctorName,
            "bookingID": self.bookingID,
            "clinicName": self.clinicName,
            "patientID": self.patientID,
            "patientName": self.patientName,
            "bookingDate": self.bookingDate,
            "timeStamp": self.timeStamp,
            "ratingGiven": self.ratingGiven,
            "comments": self.comments,
        }