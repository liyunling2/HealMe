from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from models import DoctorRating, ClinicRating
from db import db
from utils import get_filtered_query_from_args
import traceback
import uuid

routes = Blueprint("rating", __name__)

@routes.route("/doctors", methods=["GET"])
def get_doc_ratings():
    args = request.args
    try:
        ratings = DoctorRating.query.filter_by(**args).all()
        return jsonify({"data": [rating.json() for rating in ratings]}), 200
    
    except InvalidRequestError as e:
        return jsonify({"message": "Bad request: " + str(e)}), 400
    
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return jsonify({"message": "An error occurred retrieving doctor ratings."}), 500

@routes.route("/clinics", methods=["GET"])
def get_clinic_ratings():
    args = request.args
    try:
        ratings = ClinicRating.query.filter_by(**args).all()
        return jsonify({"data": [rating.json() for rating in ratings]}), 200
    
    except InvalidRequestError as e:
        return jsonify({"message": "Bad request: " + str(e)}), 400
   
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return jsonify({"message": "An error occurred retrieving clinic ratings."}), 500

@routes.route("/doctors", methods=["POST"])
def rate_doctor():
    try:
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
    
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Duplicate rating not allowed"}), 400
    
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return jsonify({"message": "An error occurred creating the doctor rating."}), 500

@routes.route("/clinics", methods=["POST"])
def rate_clinic():
    try:
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
    
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Duplicate rating not allowed"}), 400
    
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return jsonify({"message": "An error occurred creating the clinic rating."}), 500