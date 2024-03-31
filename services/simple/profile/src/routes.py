from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from models import Patient, Doctor
from db import db
import traceback
import json
import uuid

routes = Blueprint("profile", __name__)

#patient routes

@routes.route("/patients/login", methods=["POST"])
def patient_login():
    try:
        data = request.get_json()
        patient = Patient.query.filter_by(email=data.get('email')).first()
        if patient and patient.password == data.get('password'):
            return jsonify({"data": patient.json(), "message": "Patient logged in successfully."}), 200
        else:
            return jsonify({"data": None, "message": "Invalid email or password."}), 401
    
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return jsonify({"data": None, "message": "An error occurred logging in the patient."}), 500

@routes.route("/patients", methods=["GET"])
def get_patients():
    try:
        patient_name = request.args.get('patientName')
        if patient_name:
            patient = Patient.query.filter_by(patientName=patient_name).first()
            return jsonify({"data": patient.json() if patient else None, "message": "Patient retrieved successfully." if patient else "Patient not found"}), 200 if patient else 404
        else:
            patients = Patient.query.all()
            return jsonify({"data": [patient.json() for patient in patients] or [], "message": "Patients retrieved successfully."}), 200
    
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return jsonify({"data": None, "message": "An error occurred retrieving the patients."}), 500

@routes.route("/patients/<string:patientID>", methods=["GET"])
def get_patient_by_id(patientID):
    try:
        patient = Patient.query.get(patientID)
        return jsonify({"data": patient.json() if patient else None, "message": "Patient retrieved successfully." if patient else "Patient not found"}), 200 if patient else 404
    
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return jsonify({"data": None, "message": "An error occurred retrieving the patient."}), 500

@routes.route("/patients/<string:patientID>", methods=["PUT"])
def edit_patient_profile(patientID):
    try:
        patient = Patient.query.get(patientID)
        if patient:
            data = request.get_json()
            patient.patientName = data.get('patientName', patient.patientName)
            patient.contactNum = data.get('contactNum', patient.contactNum)
            patient.email = data.get('email', patient.email)
            patient.password = data.get('password', patient.password)
            # patient.allergies = json.dumps(data.get('allergies', json.loads(patient.allergies)))
            # patient.medications = json.dumps(data.get('medications', json.loads(patient.medications)))
            db.session.commit()
            return jsonify({"data": patient.json(), "message": "Patient profile updated successfully."}), 200
        else:
            return jsonify({"data": None, "message": "Patient not found"}), 404
    
    except IntegrityError:
        db.session.rollback()
        return jsonify({"data": None, "message": "Update failed due to a data conflict or constraint violation."}), 400
    
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return jsonify({"data": None, "message": "An error occurred updating the patient profile."}), 500

@routes.route("/patients", methods=["POST"])
def add_patient_profile():
    try:
        data = request.get_json()
        new_patient = Patient(patientID=str(uuid.uuid4()),
            email=data.get('email'),
            password=data.get('password'),
            patientName=data.get('patientName'), 
            contactNum=data.get('contactNum'))
        db.session.add(new_patient)
        db.session.commit()
        return jsonify({"data": new_patient.json(), "message": "Patient profile added successfully."}), 201
    
    except IntegrityError:
        db.session.rollback()
        return jsonify({"data": None, "message": "Duplicate patient data or constraint violation."}), 400
    
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return jsonify({"data": None, "message": "An error occurred creating the patient profile."}), 500


#doctor routes

@routes.route("/doctors/login", methods=["POST"])
def doctor_login():
    try:
        data = request.get_json()
        doctor = Doctor.query.filter_by(email=data.get('email')).first()
        if doctor and doctor.password == data.get('password'):
            return jsonify({"data": doctor.json(), "message": "Doctor logged in successfully."}), 200
        else:
            return jsonify({"data": None, "message": "Invalid email or password."}), 401
    
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return jsonify({"data": None, "message": "An error occurred logging in the doctor."}), 500

@routes.route("/doctors", methods=["GET"])
def get_doctors():
    try:
        doctor_name = request.args.get('doctorName')
        clinic_id = request.args.get('clinicID')
        query = Doctor.query
        if doctor_name:
            query = query.filter(Doctor.doctorName.ilike(f"%{doctor_name}%"))
        if clinic_id:
            query = query.filter_by(clinicID=clinic_id)
        doctors = query.all()
        return jsonify({"data": [doctor.json() for doctor in doctors] or [], "message": "Doctors retrieved successfully."}), 200
    
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return jsonify({"data": None, "message": "An error occurred retrieving the doctors."}), 500

@routes.route("/doctors/<string:doctorID>", methods=["GET"])
def get_doctor_profile(doctorID):
    try:
        doctor = Doctor.query.get(doctorID)
        return jsonify({"data": doctor.json() if doctor else None, "message": "Doctor profile retrieved successfully." if doctor else "Doctor not found"}), 200 if doctor else 404
    
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return jsonify({"data": None, "message": "An error occurred retrieving the doctor profile."}), 500


@routes.route("/doctors/<string:doctorID>", methods=["PUT"])
def edit_doctor_profile(doctorID):
    try:
        doctor = Doctor.query.get(doctorID)
        if doctor:
            data = request.get_json()
            doctor.doctorName = data.get('doctorName', doctor.doctorName)
            doctor.doctorDesc = data.get('doctorDesc', doctor.doctorDesc)
            doctor.specialty = data.get('specialty', doctor.specialty)
            db.session.commit()
            return jsonify({"data": doctor.json(), "message": "Doctor profile updated successfully."}), 200
        
        else:
            return jsonify({"data": None, "message": "Doctor not found"}), 404
    
    except IntegrityError:
        db.session.rollback()
        return jsonify({"data": None, "message": "Update failed due to a data conflict or constraint violation."}), 400
    
    except Exception as e:
        return jsonify({"data": None, "message": "An error occurred updating the doctor profile."}), 500

@routes.route("/doctors", methods=["POST"])
def add_doctor_profile():
    try:
        data = request.get_json()
        new_doctor = Doctor(clinicID=data.get('clinicID'), email=data.get('email'), password=data.get('password'),
                        doctorID=str(uuid.uuid4()), doctorName=data.get('doctorName'), 
                        doctorDesc=data.get('doctorDesc'), specialty=data.get('specialty'))
        db.session.add(new_doctor)
        db.session.commit()
        return jsonify({"data": new_doctor.json(), "message": "Doctor profile added successfully."}), 201
    
    except IntegrityError:
        db.session.rollback()
        return jsonify({"data": None, "message": "Duplicate doctor data or constraint violation."}), 400
    
    except Exception as e:
        return jsonify({"data": None, "message": "An error occurred creating the doctor profile."}), 500
