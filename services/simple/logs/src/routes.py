from flask import Blueprint, request, jsonify
from models import Logs
from db import db
import json
import uuid

routes = Blueprint("logs", __name__)

@routes.route("/")
def index():
    return "Log service is running"

#booking routes

#EXTRACT BOOKING, CAN FILTER AS SUCH http://127.0.0.1:5005/bookings?patientID=101&dateOfBooking=2024-03-01
@routes.route("/logs", methods=["GET"])
def get_logs():
    # Extract parameters from the request
    
    log_ID = request.args.get('logID')
    log_date = request.args.get('logDate')
    log_type = request.args.get('logType')

    # Define filter conditions based on the provided parameters
    filters = []
    if log_ID:
        filters.append(Logs.logID == log_ID)
    if log_date:
        filters.append(Logs.logDate == log_date)
    if log_type:
        filters.append(Logs.logType == log_type)

    # Apply filters to the query
    if filters:
        logs = Logs.query.filter(*filters).all()
    else:
        logs = Logs.query.all()

    # Return the result with appropriate HTTP status code
    if logs:
        return jsonify([logs.json() for log in logs]), 200
    else:
        return jsonify({"message": "Log not found"}), 404

#EDIT A LOG BY LOGID
@routes.route("/logs/<string:logID>", methods=["PUT"])
def edit_log(logID):
    log = Logs.query.get(logID)
    if log:
        data = request.get_json()
        log.logID = data.get('logID', log.logID)
        log.logDate = data.get('logDate', log.logDate)
        log.logType = data.get('logType', log.logType)
        db.session.commit()
        return jsonify(log.json()), 200
    return jsonify({"message": "Log not found"}), 404

#ADD A LOG
@routes.route("/logs", methods=["POST"])
def add_log():
    data = request.get_json()
    new_log = Logs(bookingID=str(uuid.uuid4()), 
        logID=data.get('logID'), 
        logDate=data.get('logDate'), 
        logType=data.get('logType'),
        )
    db.session.add(new_log)
    db.session.commit()
    return jsonify(new_log.json()), 201

#DELETE LOG BY LOGID
@routes.route("/logs/<string:logID>", methods=["DELETE"])
def delete_log(logID):
    log = Logs.query.get(logID)
    if log:
        db.session.delete(log)
        db.session.commit()
        return jsonify({"message": "Log deleted successfully"}), 200
    return jsonify({"message": "Log not found"}), 404
