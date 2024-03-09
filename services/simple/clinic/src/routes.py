from flask import Blueprint, request, jsonify
from models import Clinic
from db import db
import json
import uuid

routes = Blueprint("clinic", __name__)

#remove after testing
@routes.route("/clinics/all", methods=["DELETE"])
def delete_all_clinics():
    try:
        num_deleted = db.session.query(Clinic).delete()
        db.session.commit()
        return jsonify({"message": f"Successfully deleted {num_deleted} clinic(s)."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@routes.route("/clinics", methods=["GET"])
def get_clinics():
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

@routes.route("/clinics/<string:clinicID>", methods=["GET"])
def get_clinic_by_id(clinicID):
    clinic = Clinic.query.get(clinicID)
    return jsonify(clinic.json()) if clinic else jsonify({"message": "Clinic not found"}), 404

@routes.route("/clinics", methods=["POST"])
def add_clinic():
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

@routes.route("/clinics/<string:clinicID>", methods=["PUT"])
def edit_clinic(clinicID):
    clinic = Clinic.query.get(clinicID)
    if clinic:
        data = request.json
        clinic.clinicName = data.get('clinicName', clinic.clinicName)
        clinic.location = data.get('location', clinic.location)
        clinic.services = json.dumps(data.get('services', json.loads(clinic.services)))
        db.session.commit()
        return jsonify(clinic.json()), 200
    return jsonify({"message": "Clinic not found"}), 404