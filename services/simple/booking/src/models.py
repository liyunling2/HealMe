from db import db
import json
import uuid

class Booking(db.Model):
    __tablename__ = "booking"
    
    bookingID = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patientID = db.Column(db.String(36))
    clinicID = db.Column(db.String(36))
    doctorID = db.Column(db.String(36))
    date = db.Column(db.Date)
    slotNo = db.Column(db.Integer)
    bookingStatus = db.Column(db.VARCHAR(255))

    __table_args__ = (db.CheckConstraint('slotNo >= 1 and slotNo <= 24', name='slotNo_check'),
                      db.UniqueConstraint('doctorID', 'date', 'slotNo', name='doctorID_date_slotNo'),)

    def json(self):
        return {
            "bookingID": self.bookingID,
            "patientID": self.patientID,
            "clinicID": self.clinicID,
            "doctorID": self.doctorID,
            "date": self.date,
            "slotNo": self.slotNo,
            "bookingStatus": self.bookingStatus,
            
        }
