from flask import Blueprint, request, jsonify
from models import Patient, Doctor
from db import db
import json
import uuid

routes = Blueprint("profile", __name__)

@routes.route("/")
def index():
    print("Profile service is running")
    return "Profile service is running"

#patient routes
@routes.route("/patients", methods=["GET"])
def get_all_patients():
    patients = Patient.query.all()
    return jsonify([patient.json() for patient in patients]), 200

@routes.route("/patients/<string:patientID>", methods=["GET"])
def get_patient_by_id(patientID):
    patient = Patient.query.get(patientID)
    if patient:
        return jsonify(patient.json()), 200
    return jsonify({"message": "Patient not found"}), 404

@routes.route("/patients", methods=["GET"])
def get_patient_by_name():
    patient_name = request.args.get('patientName')
    patient = Patient.query.filter_by(patientName=patient_name).first()
    if patient:
        return jsonify(patient.json()), 200
    return jsonify({"message": "Patient not found"}), 404

@routes.route("/patients/<string:patientID>", methods=["PUT"])
def edit_patient_profile(patientID):
    patient = Patient.query.get(patientID)
    if patient:
        data = request.get_json()
        patient.patientName = data.get('patientName', patient.patientName)
        patient.contactNum = data.get('contactNum', patient.contactNum)
        patient.allergies = json.dumps(data.get('allergies', []))
        patient.medications = json.dumps(data.get('medication', []))
        db.session.commit()
        return jsonify(patient.json()), 200
    return jsonify({"message": "Patient not found"}), 404

@routes.route("/patients", methods=["POST"])
def add_patient_profile():
    data = request.get_json()
    new_patient = Patient(patientID=str(uuid.uuid4()), **data)
    db.session.add(new_patient)
    db.session.commit()
    return jsonify(new_patient.json()), 201

#doctor routes
@routes.route("/doctors", methods=["GET"])
def get_all_doctors():
    clinic_id = request.args.get('clinicID')
    if clinic_id:
        doctors = Doctor.query.filter_by(clinicID=clinic_id).all()
    else:
        doctors = Doctor.query.all()
    return jsonify([doctor.json() for doctor in doctors]), 200

@routes.route("/doctors/<string:doctorID>", methods=["GET"])
def get_doctor_profile(doctorID):
    doctor = Doctor.query.get(doctorID)
    if doctor:
        return jsonify(doctor.json()), 200
    return jsonify({"message": "Doctor not found"}), 404

@routes.route("/doctors", methods=["PUT"])
def edit_doctor_profile():
    doctor_id = request.args.get('doctorID')
    doctor = Doctor.query.get(doctor_id)
    if doctor:
        data = request.get_json()
        doctor.doctorName = data.get('doctorName', doctor.doctorName)
        doctor.doctorDesc = data.get('doctorDesc', doctor.doctorDesc)
        doctor.specialty = data.get('specialty', doctor.specialty)
        doctor.ratings = data.get('ratings', doctor.ratings)
        db.session.commit()
        return jsonify(doctor.json()), 200
    return jsonify({"message": "Doctor not found"}), 404

@routes.route("/doctors", methods=["POST"])
def add_doctor_profile():
    data = request.get_json()
    new_doctor = Doctor(**data)
    db.session.add(new_doctor)
    db.session.commit()
    return jsonify(new_doctor.json()), 201