from db import db

class BlockedSlot(db.Model):
    __tablename__ = 'blocked_slots'
    
    id = db.Column(db.Integer, primary_key=True)
    doctorId = db.Column(db.String(255))
    clinicId = db.Column(db.String(255))
    date = db.Column(db.Date)
    slotNo = db.Column(db.Integer)
    reason = db.Column(db.String(255))

    # unique constraint for doctorID, date, and slotNo
    __table_args__ = (db.UniqueConstraint('doctorId', 'date', 'slotNo', name='unique_slot'),)

    def json(self):
        return {
            'id': self.id,
            'doctorId': self.doctorId,
            'clinicId': self.clinicId,
            'date': self.date,
            'slotNo': self.slotNo,
            'reason': self.reason
        }