from db import db

class ScheduleItem(db.Model):
    __tablename__ = "schedule_item"
    id = db.Column(db.Integer, primary_key=True)
    bookerID = db.Column(db.Integer)
    date = db.Column(db.Date)
    slotNo = db.Column(db.Integer)
    itemType = db.Column(db.String)

    __mapper_args__ = {
        "polymorphic_identity": "schedule_item",
        "polymorphic_on": itemType
    }

    def json(self):
        return {
            "id": self.id,
            "bookerID": self.bookerID,
            "date": self.date,
            "slotNo": self.slotNo,
            "itemType": self.itemType
        }

    def __init__(self, bookerID, date, slotNo):
        self.bookerID = bookerID
        self.date = date
        self.slotNo = slotNo

class Booking(ScheduleItem):
    __tablename__ = "booking"
    scheduleSlotId = db.Column(db.Integer, db.ForeignKey("schedule_item.id"), primary_key=True)
    doctorID = db.Column(db.Integer, primary_key=True)
    doctorName = db.Column(db.String)
    name = db.Column(db.String)
    contactNum = db.Column(db.Integer)
    allergies = db.Column(db.ARRAY(db.String))
    medications = db.Column(db.ARRAY(db.String))
    # paymentInformation = db.Column(db.Integer)
    __mapper_args__ = {
        "polymorphic_identity": "booking"
    }
    
    def json(self):
        return {
            "scheduleSlotId": self.scheduleItemId,
            "doctorID": self.doctorID,
            "patientName": self.name,
            "doctorName": self.doctorName,
            "contactNum": self.contactNum,
            "allergies": self.allergies,
            "medications": self.medications
        } | super().json()

class BlockedSlot(ScheduleItem):
    __tablename__ = "blocked_slot"
    scheduleSlotId = db.Column(db.Integer, db.ForeignKey("schedule_item.id"), primary_key=True)
    reason = db.Column(db.String)

    __mapper_args__ = {
        "polymorphic_identity": "blocked_slot"
    }
    
    def json(self):
        return {
            "scheduleSlotId": self.scheduleItemId,
            "reason": self.reason
        } | super().json()
    