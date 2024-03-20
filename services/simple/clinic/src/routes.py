from flask import Blueprint, request, jsonify
from models import Clinic
from db import db
import traceback
import json
import uuid

routes = Blueprint("clinic", __name__)

#remove after testing
@routes.route("/all", methods=["DELETE"])
def delete_all_clinics():
    try:
        num_deleted = db.session.query(Clinic).delete()
        db.session.commit()
        return jsonify({"message": f"Successfully deleted {num_deleted} clinic(s)."}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

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
        return jsonify([clinic.json() for clinic in clinics]), 200
    
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return jsonify({"message": "An error occurred retrieving the clinics."}), 400

@routes.route("/<string:clinicID>", methods=["GET"])
def get_clinic_by_id(clinicID):
    try:
        clinic = Clinic.query.get(clinicID)
        return jsonify(clinic.json()) if clinic else jsonify({"message": "Clinic not found"}), 404
    
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return jsonify({"message": "An error occurred retrieving the clinic."}), 400


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
        return jsonify(clinic.json()), 201
    
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return jsonify({"message": "An error occurred creating the clinic."}), 500


@routes.route("/<string:clinicID>", methods=["PUT"])
def edit_clinic(clinicID):
    try:
        clinic = Clinic.query.get(clinicID)
        if clinic:
            data = request.json
            clinic.clinicName = data.get('clinicName', clinic.clinicName)
            clinic.location = data.get('location', clinic.location)
            clinic.services = json.dumps(data.get('services', json.loads(clinic.services)))
            db.session.commit()
            return jsonify(clinic.json()), 200
        return jsonify({"message": "Clinic not found"}), 404
    
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return jsonify({"message": "An error occurred updating the clinic."}), 500