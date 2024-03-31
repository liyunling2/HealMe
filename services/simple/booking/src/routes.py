from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from models import Booking
from db import db
import traceback

routes = Blueprint("booking", __name__)

@routes.route("/", methods=["GET"])
def get_bookings():
    try:
        bookings = Booking.query.filter_by(**request.args).all()
        if not bookings:
            return jsonify({"data": [], "message": "No bookings found."}), 200
        else:
            return jsonify({"data": [booking.json() for booking in bookings], "message": "Bookings retrieved successfully."}), 200

    except InvalidRequestError as e:
        return jsonify({"data": None, "message": "Invalid query parameters."}), 400

    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return jsonify({"data": None, "message": "An error occurred retrieving the bookings."}), 500
    
@routes.route("/<string:bookingID>", methods=["GET"])
def get_bookings_by_ID(bookingID):
    try:
        booking = Booking.query.get(bookingID)
        if booking:
            return jsonify({"data": booking.json(), "message": "Booking retrieved successfully."}), 200
        else:
            return jsonify({"data": None, "message": "Booking not found"}), 404
        
    except InvalidRequestError as e:
        return jsonify({"data": None, "message": "Invalid request." + str(e)}), 400
    
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return jsonify({"data": None, "message": "An error occurred retrieving the booking."}), 500

@routes.route("/<string:bookingID>", methods=["PUT"])
def edit_booking(bookingID):
    try:
        booking = Booking.query.get(bookingID)

        if booking:
            data = request.get_json()
            try:
                for key, value in data.items():
                    setattr(booking, key, value if value is not None else getattr(booking, key))
                db.session.commit()
                return jsonify({"data": booking.json(), "message": "Booking updated successfully."}), 200
            
            except IntegrityError:
                db.session.rollback()
                return jsonify({"data": None, "message": "Update failed due to a data conflict."}), 400
        else:
            return jsonify({"data": None, "message": "Booking not found"}), 404
    
    except InvalidRequestError as e:
        return jsonify({"data": None, "message": "Invalid request data."}), 400

    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return jsonify({"data": None, "message": "An error occurred updating the booking."}), 500

@routes.route("/<string:bookingID>", methods=["PATCH"])
def patch_booking(bookingID):
    data = request.get_json()
    booking = Booking.query.get(bookingID)
    
    try: 
        if booking:
            for key, value in data.items():
                setattr(booking, key, value if value is not None else getattr(booking, key))
            db.session.commit()
            return {
                "data": booking.json(),
                "message": "Booking status changed to Completed"
            }, 200

        return {"message": "Booking not found"}, 404

    except Exception as e:
        return {"message": str(e)}, 400

@routes.route("/", methods=["POST"])
def add_booking():
    try: 
        data = request.get_json()

        if data.get("bookingID"):
            del data["bookingID"]

        data["bookingStatus"] = "Confirmed"

        new_booking = Booking(**data)
        db.session.add(new_booking)
        db.session.commit()

    except IntegrityError:
        return jsonify({"data": None, "message": "Booking Slot already taken"}), 400

    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return jsonify({"data": None, "message": "An error occurred creating the booking."}), 500
    
    return jsonify({"data": new_booking.json(), "message": "Booking created successfully."}), 201

@routes.route("/<string:bookingID>", methods=["DELETE"])
def delete_booking(bookingID):
    try:
        booking = Booking.query.get(bookingID)
        if booking:
            db.session.delete(booking)
            db.session.commit()
            return jsonify({"data": None, "message": "Booking deleted successfully"}), 200
        else:
            return jsonify({"data": None, "message": "Booking not found"}), 404
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"data": None, "message": "An error occurred deleting the booking."}), 500

@routes.route("/", methods=["DELETE"])
def delete_booking_by_param():
    try:
        num_deleted = db.session.query(Booking).filter_by(**request.args).delete()
        db.session.commit()
        message = "Successfully deleted {} booking(s)." if num_deleted else "No bookings found matching criteria."
        return jsonify({"data": None, "message": message.format(num_deleted)}), 200 if num_deleted else 404
    
    except InvalidRequestError as e:
        db.session.rollback()
        return jsonify({"message": "Invalid deletion request."}), 400
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"data": None, "message": "An error occurred during the delete operation."}), 500

#FOR TESTING PURPOSES
@routes.route("/all", methods=["DELETE"])
def delete_all_bookings():
    try:
        num_deleted = db.session.query(Booking).delete()
        db.session.commit()
        return jsonify({"data": None, "message": f"Successfully deleted {num_deleted} bookings."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"data": None, "message": "An error occurred deleting all bookings."}), 500