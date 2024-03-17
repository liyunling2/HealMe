from db import db
import json

class Logs(db.Model):
    __tablename__ = "logs"
    logID = db.Column(db.String(36), primary_key=True)
    logDate = db.Column(db.DateTime)
    logType = db.Column(db.String(36))
    logDesc = db.Column(db.String(36))

    def __init__(self, logID, logDate, logType, logDesc):
        self.logID = logID
        self.logDate = logDate
        self.logType = logType
        self.logDesc = logDesc

    def json(self):
        return {
            "logID": self.logID,
            "logDate": self.logDate,
            "logType": self.logType,
            "logDesc": self.logDesc,
        }
