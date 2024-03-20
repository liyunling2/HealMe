from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from models import Booking
from db import db
import traceback

routes = Blueprint("booking", __name__)

@routes.route("/", methods=["GET"])
def get_bookings():
    try:
        bookings = Booking.query.filter_by(**request.args).all()
        return jsonify({ "data": [booking.json() for booking in bookings] }), 200

    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return jsonify({"message": "An error occurred retrieving the bookings."}), 400

@routes.route("/<string:bookingID>", methods=["PUT"])
def edit_booking(bookingID):
    try:
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
        else:
            return jsonify({"message": "Booking not found"}), 404
    
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return jsonify({"message": "An error occurred updating the booking."}), 500

@routes.route("/", methods=["POST"])
def add_booking():
    try: 
        data = request.get_json()
        
        if not all(key in data for key in ['patientID', 'doctorID', 'clinicID', 'date']):
            return jsonify({"message": "Missing required booking information."}), 400

        if data.get("bookingID"):
            del data["bookingID"]

        new_booking = Booking(**data)
        db.session.add(new_booking)
        db.session.commit()
        return jsonify(new_booking.json()), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Booking Slot already taken"}), 400

    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return jsonify({"message": "An error occurred creating the booking."}), 500

#DELETE BOOKING BY BOOKINGID
@routes.route("/<string:bookingID>", methods=["DELETE"])
def delete_booking(bookingID):
    booking = Booking.query.get(bookingID)
    if booking:
        db.session.delete(booking)
        db.session.commit()
        return jsonify({"message": "Booking deleted successfully"}), 200
    return jsonify({"message": "Booking not found"}), 404


#FOR TESTING PURPOSES
@routes.route("/all", methods=["DELETE"])
def delete_all_bookings():
    try:
        num_deleted = db.session.query(Booking).delete()
        db.session.commit()
        return jsonify({"message": f"Successfully deleted {num_deleted} patient(s)."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500