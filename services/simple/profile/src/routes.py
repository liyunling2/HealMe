from flask import Blueprint, request, jsonify
from models import Patient, Doctor
from db import db
import json
import uuid

routes = Blueprint("profile", __name__)

@routes.route("/")
def index():
    return "Profile service is running"

#remove after testing
@routes.route("/patients/all", methods=["DELETE"])
def delete_all_patients():
    try:
        num_deleted = db.session.query(Patient).delete()
        db.session.commit()
        return jsonify({"message": f"Successfully deleted {num_deleted} patient(s)."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

#patient routes
@routes.route("/patients", methods=["GET"])
def get_patients():
    patient_name = request.args.get('patientName')
    if patient_name:
        patient = Patient.query.filter_by(patientName=patient_name).first()
        return jsonify(patient.json()) if patient else jsonify({"message": "Patient not found"}), 404
    else:
        patients = Patient.query.all()
        return jsonify([patient.json() for patient in patients]), 200

@routes.route("/patients/<string:patientID>", methods=["GET"])
def get_patient_by_id(patientID):
    patient = Patient.query.get(patientID)
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
        patient.allergies = json.dumps(data.get('allergies', json.loads(patient.allergies)))
        patient.medications = json.dumps(data.get('medication', json.loads(patient.medications)))
        db.session.commit()
        return jsonify(patient.json()), 200
    return jsonify({"message": "Patient not found"}), 404

@routes.route("/patients", methods=["POST"])
def add_patient_profile():
    data = request.get_json()
    new_patient = Patient(patientID=str(uuid.uuid4()), patientName=data.get('patientName'), 
        contactNum=data.get('contactNum'), allergies=json.dumps(data.get('allergies')), 
        medications=json.dumps(data.get('medication')))
    db.session.add(new_patient)
    db.session.commit()
    return jsonify(new_patient.json()), 201

#doctor routes
@routes.route("/doctors", methods=["GET"])
def get_doctors():
    doctor_name = request.args.get('doctorName')
    clinic_id = request.args.get('clinicID')
    if doctor_name:
        doctor = Doctor.query.filter_by(doctorName=doctor_name).first()
        return jsonify(doctor.json()) if doctor else jsonify({"message": "Doctor not found"}), 404
    elif clinic_id:
        doctors = Doctor.query.filter_by(clinicID=clinic_id).all()
        return jsonify([doctor.json() for doctor in doctors]), 200
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
    new_doctor = Doctor(clinicID=data.get('clinicID'), doctorID=str(uuid.uuid4()), doctorName=data.get('doctorName'), 
                    doctorDesc=data.get('doctorDesc'), specialty=data.get('specialty'), ratings=data.get('ratings'))
    db.session.add(new_doctor)
    db.session.commit()
    return jsonify(new_doctor.json()), 201