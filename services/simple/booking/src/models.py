from db import db
import json
import uuid

class Booking(db.Model):
    __tablename__ = "booking"
    
    bookingID = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patientID = db.Column(db.String(36))
    patientName = db.Column(db.String(36))
    patientEmail = db.Column(db.String(36))
    doctorID = db.Column(db.String(36))
    doctorName = db.Column(db.String(36))
    doctorEmail = db.Column(db.String(36))
    clinicID = db.Column(db.String(36))
    clinicName = db.Column(db.String(36))
    clinicLocation = db.Column(db.String(36))
    date = db.Column(db.DateTime)
    slotNo = db.Column(db.Integer)
    bookingStatus = db.Column(db.VARCHAR(255))

    __table_args__ = (db.CheckConstraint('slotNo >= 1 and slotNo <= 24', name='slotNo_check'),
                      db.UniqueConstraint('doctorID', 'date', 'slotNo', name='doctorID_date_slotNo'), 
                      db.UniqueConstraint('patientID', 'date', 'slotNo'))

    def json(self):
        return {
            "bookingID": self.bookingID,
            "patientID": self.patientID,
            "patientName": self.patientName,
            "patientEmail": self.patientEmail,
            "doctorID": self.doctorID,
            "doctorName": self.doctorName,
            "doctorEmail": self.doctorEmail,
            "clinicID": self.clinicID,
            "clinicName": self.clinicName,
            "clinicLocation": self.clinicLocation,
            "date": self.date,
            "slotNo": self.slotNo,
            "bookingStatus": self.bookingStatus,
        }
