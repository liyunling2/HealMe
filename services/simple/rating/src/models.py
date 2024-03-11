from db import db

class ClinicRating(db.Model):
    __tablename__ = 'clinic_rating'
    
    ratingID = db.Column(db.String(36), primary_key=True)
    clinicID = db.Column(db.String(36))
    ratingGiven = db.Column(db.Float)
    timeStamp = db.Column(db.DateTime)
    ratingComment = db.Column(db.VARCHAR(255))


    def __init__(self, ratingID, clinicID, ratingGiven, timeStamp, ratingComment):
        self.ratingID = ratingID
        self.clinicID = clinicID
        self.ratingGiven = ratingGiven
        self.timeStamp = timeStamp
        self.ratingComment = ratingComment

    def json(self):
        return {
            "ratingID": self.ratingID,
            "clinicID": self.clinicID,
            "ratingGiven": self.ratingGiven,
            "timeStamp": self.timeStamp,
            "ratingComment": self.ratingComment,
        }
    
class DoctorRating(db.Model):
    __tablename__ = 'doctor_rating'
    
    ratingID = db.Column(db.String(36), primary_key=True)
    clinicID = db.Column(db.String(36))
    doctorID = db.column(db.string(36))
    appointmentID = db.column(db.string(36))
# not sure how to do foreign key
    ratorID = db.Column(db.Integer, db.ForeignKey("??"))
    ratingGiven = db.Column(db.Float)
    timeStamp = db.Column(db.DateTime)
    ratingComment = db.Column(db.VARCHAR(255))


    def __init__(self, ratingID, clinicID, doctorID, appointmentID, ratorID, ratingGiven, timeStamp, ratingComment):
        self.ratingID = ratingID
        self.clinicID = clinicID
        self.doctorID = doctorID
        self.appointmentID = appointmentID
        self.ratorID = ratorID
        self.ratingGiven = ratingGiven
        self.timeStamp = timeStamp
        self.ratingComment = ratingComment

    def json(self):
        return {
            "ratingID": self.ratingID,
            "clinicID": self.clinicID,
            "doctorID": self.doctorID,
            "appointmentID": self.appointmentID,
            "ratorID": self.ratorID,
            "ratingGiven": self.ratingGiven,
            "timeStamp": self.timeStamp,
            "ratingComment": self.ratingComment,
        }