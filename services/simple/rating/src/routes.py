from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from models import DoctorRating, ClinicRating
from db import db
from utils import get_filtered_query_from_args
import uuid

routes = Blueprint("rating", __name__)

@routes.route("/doctors", methods=["GET"])
def get_doc_ratings():
    args = request.args
    try:
        slots = DoctorRating.query.filter_by(**args).all()
    except InvalidRequestError as e:
        return {
            "message": "Bad request: " + str(e)
        }, 400

    return {
        "data": [slot.json() for slot in slots]
    }

@routes.route("/clinics", methods=["GET"])
def get_clinic_ratings():
    args = request.args
    try:
        slots = ClinicRating.query.filter_by(**args).all()
    except InvalidRequestError as e:
        return {
            "message": "Bad request: " + str(e)
        }, 400

    return {
        "data": [slot.json() for slot in slots]
    }

@routes.route("/doctors", methods=["POST"])
def rate_doctor():
    data = request.json
    rating = DoctorRating(
        ratingID=str(uuid.uuid4()),
        clinicID=data['clinicID'],
        doctorID=data['doctorID'],
        appointmentID=data['appointmentID'],
        ratorID=data['ratorID'],
        ratingGiven=data['ratingGiven'],
        ratingComment=data['ratingComment'],
        timeStamp=data['timeStamp']
    )
    db.session.add(rating)
    db.session.commit()
    return jsonify(rating.json()), 201

@routes.route("/clinics", methods=["POST"])
def rate_clinic():
    data = request.json
    rating = ClinicRating(
        ratingID=str(uuid.uuid4()),
        clinicID=data['clinicID'],
        ratorID=data['ratorID'],
        ratingGiven=data['ratingGiven'],
        ratingComment=data['ratingComment'],
        timeStamp=data['timeStamp']
    )
    db.session.add(rating)
    db.session.commit()
    return jsonify(rating.json()), 201