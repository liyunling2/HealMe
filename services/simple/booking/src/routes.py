from flask import Blueprint, request, jsonify
from models import Booking
from db import db
import json
import uuid

routes = Blueprint("booking", __name__)

@routes.route("/")
def index():
    return "Booking service is running"

#booking routes

#EXTRACT BOOKING, CAN FILTER AS SUCH http://127.0.0.1:5005/bookings?patientID=101&dateOfBooking=2024-03-01
@routes.route("/bookings", methods=["GET"])
def get_bookings():
    # Extract parameters from the request
    clinic_id = request.args.get('clinicID')
    doctor_id = request.args.get('doctorID')
    patient_id = request.args.get('patientID')
    date_of_booking = request.args.get('dateOfBooking')
    booking_status = request.args.get('bookingStatus')
    booking_id = request.args.get('bookingID')

    # Define filter conditions based on the provided parameters
    filters = []
    if clinic_id:
        filters.append(Booking.clinicID == clinic_id)
    if doctor_id:
        filters.append(Booking.doctorID == doctor_id)
    if patient_id:
        filters.append(Booking.patientID == patient_id)
    if date_of_booking:
        filters.append(Booking.dateOfBooking == date_of_booking)
    if booking_status:
        filters.append(Booking.bookingStatus == booking_status)
    if booking_id:
        filters.append(Booking.bookingID == booking_id)

    # Apply filters to the query
    if filters:
        bookings = Booking.query.filter(*filters).all()
    else:
        bookings = Booking.query.all()

    # Return the result with appropriate HTTP status code
    if bookings:
        return jsonify([booking.json() for booking in bookings]), 200
    else:
        return jsonify({"message": "Booking not found"}), 404

#EDIT A BOOKING BY BOOKINGID
@routes.route("/bookings/<string:bookingID>", methods=["PUT"])
def edit_booking(bookingID):
    booking = Booking.query.get(bookingID)
    if booking:
        data = request.get_json()
        booking.patientID = data.get('patientID', booking.patientID)
        booking.doctorID = data.get('doctorID', booking.doctorID)
        booking.clinicID = data.get('clinicID', booking.clinicID)
        booking.dateOfBooking = data.get('dateOfBooking', booking.dateOfBooking)
        booking.bookingStatus = data.get('bookingStatus', booking.bookingStatus)
        db.session.commit()
        return jsonify(booking.json()), 200
    return jsonify({"message": "Booking not found"}), 404

#ADD A BOOKING
@routes.route("/bookings", methods=["POST"])
def add_booking():
    data = request.get_json()
    new_booking = Booking(bookingID=str(uuid.uuid4()), 
        patientID=data.get('patientID'), 
        doctorID=data.get('doctorID'), 
        clinicID=data.get('clinicID'),
        dateOfBooking=data.get('dateOfBooking'),
        bookingStatus=data.get('bookingStatus'),
        )
    db.session.add(new_booking)
    db.session.commit()
    return jsonify(new_booking.json()), 201

#DELETE BOOKING BY BOOKINGID
@routes.route("/bookings/<string:bookingID>", methods=["DELETE"])
def delete_booking(bookingID):
    booking = Booking.query.get(bookingID)
    if booking:
        db.session.delete(booking)
        db.session.commit()
        return jsonify({"message": "Booking deleted successfully"}), 200
    return jsonify({"message": "Booking not found"}), 404


#FOR TESTING PURPOSES
@routes.route("/bookings/all", methods=["DELETE"])
def delete_all_bookings():
    try:
        num_deleted = db.session.query(Booking).delete()
        db.session.commit()
        return jsonify({"message": f"Successfully deleted {num_deleted} patient(s)."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500