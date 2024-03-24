from db import db
import json

class Log(db.Model):
    __tablename__ = "log"
    logID = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    timeStamp =  db.Column(db.DateTime)
    logMsg = db.Column(db.String(255))

    def __init__(self, logID, timeStamp, logMsg):
        self.logID = logID
        self,timeStamp = timeStamp
        self.logMsg = json.dumps(logMsg)
    
    def json(self):
        return{
            "logID" : self.logID,
            "timeStamp" : self.timeStamp,
            "logMsg" : json.loads(self.logMsg) ######
        }