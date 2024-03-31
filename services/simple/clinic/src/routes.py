from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from models import Clinic
from db import db
import traceback
import json
import uuid

routes = Blueprint("clinic", __name__)

@routes.route("/", methods=["GET"])
def get_clinics():
    try:
        clinic_name = request.args.get('clinicName')
        services = request.args.get('services')
        location = request.args.get('location')
        query = Clinic.query
        if clinic_name:
            query = query.filter(Clinic.clinicName.ilike(f"%{clinic_name}%"))
        if services:
            query = query.filter(Clinic.services.contains(services))
        if location:
            query = query.filter(Clinic.location.ilike(f"%{location}%"))
        clinics = query.all()
        return jsonify({"data": [clinic.json() for clinic in clinics] or [], "message": "Clinics retrieved successfully."}), 200
    
    except InvalidRequestError as e:
        return jsonify({"data": None, "message": "Invalid query parameters."}), 400

    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return jsonify({"data": None, "message": "An error occurred retrieving the clinics."}), 500

@routes.route("/<string:clinicID>", methods=["GET"])
def get_clinic_by_id(clinicID):
    try:
        clinic = Clinic.query.get(clinicID)
        if clinic:
            return jsonify({"data": clinic.json(), "message": "Clinic retrieved successfully."}), 200
        else:
            return jsonify({"data": None, "message": "Clinic not found"}), 404

    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return jsonify({"message": "An error occurred retrieving the clinic."}), 500


@routes.route("/", methods=["POST"])
def add_clinic():
    try:
        data = request.json
        clinic = Clinic(
            clinicID=str(uuid.uuid4()),
            clinicName=data['clinicName'],
            location=data['location'],
            services=data['services']
        )
        db.session.add(clinic)
        db.session.commit()
        return jsonify({"data": clinic.json(), "message": "Clinic added successfully."}), 201
    
    except IntegrityError:
        db.session.rollback()
        return jsonify({"data": None, "message": "Duplicate clinic data or constraint violation."}), 400
    
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return jsonify({"data": None, "message": "An error occurred creating the clinic."}), 500



@routes.route("/<string:clinicID>", methods=["PUT"])
def edit_clinic(clinicID):
    try:
        clinic = Clinic.query.get(clinicID)
        if clinic:
            data = request.get_json()
            clinic.clinicName = data.get('clinicName', clinic.clinicName)
            clinic.location = data.get('location', clinic.location)
            clinic.services = json.dumps(data.get('services', json.loads(clinic.services)))
            db.session.commit()
            return jsonify({"data": clinic.json(), "message": "Clinic updated successfully."}), 200
        else:
            return jsonify({"data": None, "message": "Clinic not found"}), 404
    
    except IntegrityError:
        db.session.rollback()
        return jsonify({"data": None, "message": "Update failed due to a data conflict or constraint violation."}), 400
    
    except Exception as e:
        return jsonify({"data": None, "message": "An error occurred updating the clinic."}), 500