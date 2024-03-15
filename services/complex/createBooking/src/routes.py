from flask import Flask, Blueprint, request, jsonify
import json
import uuid

from flask_cors import CORS

import os, sys

import requests

from invokes import invoke_http

app = Flask(__name__)
CORS(app)


blocked_slots_URL = "http://localhost:5001/blocked_slots"
clinic_URL = "http://localhost:5002/clinic"
profile_URL = "http://localhost:5003/profile"
rating_URL = "http://localhost:5004/rating"
booking_URL = "http://localhost:5005/booking"

routes = Blueprint("createBooking", __name__)

@routes.route("/createBooking")
def index():
    return "createBooking service is running"

#booking routes

#EXTRACT BOOKING, CAN FILTER AS SUCH http://127.0.0.1:5005/bookings?patientID=101&dateOfBooking=2024-03-01
@routes.route("/createBooking", methods=["POST"])
def create_booking():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            createBooking = request.get_json()
            print("\nReceived a booking in JSON:", createBooking)

            # do the actual work
            # 1. Send order info {cart items}
            result = processCreateBooking(createBooking)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "place_order.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

def processCreateBooking(createBooking):
    print('\n-----Invoking booking microservice-----')
    booking_result = invoke_http(booking_URL, method='POST', json=createBooking)
    print('booking_result:', booking_result)

    # Check the order result; if a failure, send it to the error microservice.
    code = booking_result["code"]
    if code not in range(200, 300):
        # Inform the log microservice NOT DONE YET
        print('\n\n-----Invoking error microservice as order fails-----')
        invoke_http(log_URL, method="POST", json=order_result)
        # - reply from the invocation is not used; 
        # continue even if this invocation fails
        print("Order status ({:d}) sent to the log microservice:".format(code), booking_result)

        return {
            "code": 500,
            "data": {"booking_result": booking_result},
            "message": "Booking creation failure sent for error handling."
        }
    
    print('\n\n-----Invoking blocked_slots microservice-----')
    booked_slots_result = invoke_http(
        blocked_slots_URL, method="POST", json=booking_result['data'])
    print("shipping_result:", booked_slots_result, '\n')
    # Check the booked_slots result;
    # if a failure, send it to the error microservice.
    code = booked_slots_result["code"]
    if code not in range(200, 300):

        # Inform the error microservice
        print('\n\n-----Invoking error microservice as shipping fails-----')
        invoke_http(log_URL, method="POST", json=booked_slots_result)
        print("Shipping status ({:d}) sent to the error microservice:".format(
            code), booked_slots_result)

    # 7. Return error
        return {
            "code": 400,
            "data": {
                "order_result": booking_result,
                "shipping_result": booked_slots_result
            },
            "message": "Simulated booked_slots record error sent for error handling."
        }
    


    # 7. Return created booking, booked_slots record
    return {"code": 201,
        "data": {
            "order_result": booking_result,
            "shipping_result": booked_slots_result
        }
    
}
    
   






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