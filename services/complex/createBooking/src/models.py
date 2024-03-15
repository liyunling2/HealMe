from db import db
import json

class Booking(db.Model):
    __tablename__ = "booking"
    bookingID = db.Column(db.String(36), primary_key=True)
    patientID = db.Column(db.String(36))
    doctorID = db.Column(db.String(36))
    clinicID = db.Column(db.String(36))
    dateOfBooking = db.Column(db.DateTime)
    bookingStatus = db.Column(db.VARCHAR(255))

    def __init__(self, bookingID, patientID, doctorID, clinicID, dateOfBooking, bookingStatus):
        self.bookingID = bookingID
        self.patientID = patientID
        self.doctorID = doctorID
        self.clinicID = clinicID
        self.dateOfBooking = dateOfBooking
        self.bookingStatus = bookingStatus

    def json(self):
        return {
            "bookingID": self.bookingID,
            "patientID": self.patientID,
            "doctorID": self.doctorID,
            "clinicID": self.clinicID,
            "dateOfBooking": self.dateOfBooking,
            "bookingStatus": self.bookingStatus,
            
        }
