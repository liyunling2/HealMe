from db import db
import uuid

class BlockedSlot(db.Model):
    __tablename__ = 'blocked_slots'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    doctorID = db.Column(db.String(36))
    clinicID = db.Column(db.String(36))
    date = db.Column(db.Date)
    slotNo = db.Column(db.Integer)
    reason = db.Column(db.String(255))

    # unique constraint for doctorID, date, and slotNo
    __table_args__ = (db.UniqueConstraint('doctorID', 'date', 'slotNo', name='unique_slot'),)

    def json(self):
        return {
            'id': self.id,
            'doctorID': self.doctorID,
            'clinicID': self.clinicID,
            'date': self.date,
            'slotNo': self.slotNo,
            'reason': self.reason
        }