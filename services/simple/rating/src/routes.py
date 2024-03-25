from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from models import DoctorRating, ClinicRating
from db import db
import traceback
import uuid

routes = Blueprint("rating", __name__)

# @routes.route("/doctors", methods=["GET"])
# def get_doc_rating():
#     args = request.args
#     try:
#         ratings = DoctorRating.query.filter_by(**args).all()
#         return jsonify({"data": [rating.json() for rating in ratings]}), 200
    
#     except InvalidRequestError as e:
#         return jsonify({"message": "Bad request: " + str(e)}), 400
    
#     except Exception as e:
#         traceback.print_exception(type(e), e, e.__traceback__)
#         return jsonify({"message": "An error occurred retrieving doctor ratings."}), 500

@routes.route("/doctors/", methods=["GET"])
def get_doctor_rating():
    doctorID = request.args.get('doctorID')
    patientID = request.args.get('patientID')
    try:
        query = DoctorRating.query
        if doctorID:
            query = query.filter_by(doctorID=doctorID)
        if patientID:
            query = query.filter_by(patientID=patientID)
        ratings = query.all()
        return jsonify({"data": [rating.json() for rating in ratings] or [], "message": "Doctor ratings retrieved successfully."}), 200
    
    except InvalidRequestError as e:
        return jsonify({"data": None, "message": "Bad request: " + str(e)}), 400
    
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return jsonify({"data": None, "message": "An error occurred retrieving doctor rating."}), 500


# @routes.route("/clinics", methods=["GET"])
# def get_clinic_rating():
#     args = request.args
#     try:
#         ratings = ClinicRating.query.filter_by(**args).all()
#         return jsonify({"data": [rating.json() for rating in ratings]}), 200
    
#     except InvalidRequestError as e:
#         return jsonify({"message": "Bad request: " + str(e)}), 400
   
#     except Exception as e:
#         traceback.print_exception(type(e), e, e.__traceback__)
#         return jsonify({"message": "An error occurred retrieving clinic ratings."}), 500

@routes.route("/clinics/<string:clinicID>", methods=["GET"])
def get_clinic_rating(clinicID):
    try:
        ratings = ClinicRating.query.filter_by(clinicID=clinicID).all()
        return jsonify({"data": [rating.json() for rating in ratings] or [], "message": "Clinic ratings retrieved successfully."}), 200
    
    except InvalidRequestError as e:
        return jsonify({"data": None, "message": "Bad request: " + str(e)}), 400
    
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return jsonify({"data": None, "message": "An error occurred retrieving clinic ratings."}), 500

@routes.route("/doctors/<string:doctorID>", methods=["POST"])
def rate_doctor(doctorID):
    try:
        data = request.json
        rating = DoctorRating(
            ratingID=str(uuid.uuid4()),
            clinicID=data['clinicID'],
            doctorID=doctorID,
            appointmentID=data['appointmentID'],
            patientID=data['patientID'],
            ratingGiven=data['ratingGiven'],
            comments=data['comments']
            )
        db.session.add(rating)
        db.session.commit()
        return jsonify({"data": rating.json(), "message": "Doctor rated successfully."}), 201
    
    except IntegrityError:
        db.session.rollback()
        return jsonify({"data": None, "message": "Duplicate rating not allowed"}), 400
    
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return jsonify({"data": None, "message": "An error occurred creating the doctor rating."}), 500

@routes.route("/clinics", methods=["POST"])
def rate_clinic():
    try:
        data = request.json
        rating = ClinicRating(
            ratingID=str(uuid.uuid4()),
            clinicID=data['clinicID'],
            patientID=data['patientID'],
            ratingGiven=data['ratingGiven'],
            comments=data['comments']
        )
        db.session.add(rating)
        db.session.commit()
        return jsonify({"data": rating.json(), "message": "Clinic rated successfully."}), 201
    
    except IntegrityError:
        db.session.rollback()
        return jsonify({"data": None, "message": "Duplicate rating not allowed"}), 400
    
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return jsonify({"data": None, "message": "An error occurred creating the clinic rating."}), 500