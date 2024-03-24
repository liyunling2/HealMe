from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from models import Booking
from db import db
import json
import uuid

routes = Blueprint("booking", __name__)

@routes.route("/")
def index():
    return "Booking service is running"

#booking routes

#EXTRACT BOOKING, CAN FILTER AS SUCH http://127.0.0.1:5005/bookings?patientID=101&date=2024-03-01
@routes.route("/bookings", methods=["GET"])
def get_bookings():
    try:
        bookings = Booking.query.filter_by(**request.args).all()

    except Exception as e:
        return jsonify({"message": str(e)}), 400
    
    return jsonify({ "data": [booking.json() for booking in bookings] }), 200

#EDIT A BOOKING BY BOOKINGID
@routes.route("/bookings/<string:bookingID>", methods=["PUT"])
def edit_booking(bookingID):
    booking = Booking.query.get(bookingID)
    if booking:
        data = request.get_json()
        booking.patientID = data.get('patientID', booking.patientID)
        booking.doctorID = data.get('doctorID', booking.doctorID)
        booking.clinicID = data.get('clinicID', booking.clinicID)
        booking.date = data.get('date', booking.date)
        booking.bookingStatus = data.get('bookingStatus', booking.bookingStatus)
        db.session.commit()
        return jsonify(booking.json()), 200
    return jsonify({"message": "Booking not found"}), 404

#ADD A BOOKING
@routes.route("/bookings", methods=["POST"])
def add_booking():
    try: 
        data = request.get_json()

        if data.get("bookingID"):
            del data["bookingID"]

        new_booking = Booking(**data)

    
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    try:
        db.session.add(new_booking)
        db.session.commit()

    except IntegrityError as e:
        return jsonify({"message": "Booking Slot already taken"}), 400

    except Exception as e:
        print(e.with_traceback(None))
        return jsonify({"message": "An error occurred creating the booking."}), 500
    
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