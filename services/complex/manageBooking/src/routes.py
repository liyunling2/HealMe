import json
from utils import get_log_message_dict
import os
import sys
import uuid

import amqp_connection
import pika
import requests
from flask import Blueprint, Flask, jsonify, request
from flask_cors import CORS
from invokes import invoke_http

from functools import wraps

app = Flask(__name__)
CORS(app)

exchangename = "log_fanout"
exchangetype= "fanout" 

connection = amqp_connection.create_connection() 
channel = connection.channel()

def with_logging(route_handler_fn):
    @wraps(route_handler_fn)
    def with_log_fn(*args, **kwargs):
        response, code = route_handler_fn(*args, **kwargs)

        body = get_log_message_dict((response, code))
        
        channel.basic_publish(exchange=exchangename, routing_key="#",
                              body=json.dumps(body), properties=pika.BasicProperties(delivery_mode=2))
        return response
    
    return with_log_fn

BLOCKED_SLOTS_URL = os.environ.get("BLOCKED_SLOTS_URL")
# noti_URL =
BOOKING_URL = os.environ.get("BOOKING_URL")

#if the exchange is not yet created, exit the program
if not amqp_connection.check_exchange(channel, exchangename, exchangetype):
    print("\nCreate the 'Exchange' before running this microservice. \nExiting the program.")
    sys.exit(0)  # Exit with a success status

@app.route("/createBooking")
def index():
    return "createBooking Complex Microservice is running"

#booking routes

@app.route("/createBooking", methods=["POST"])
@with_logging
def create_booking():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            createBooking = request.get_json()
            print("\nReceived a booking in JSON:", createBooking)

            # create booking
            result = processCreateBooking(createBooking)
            
            print('\n------------------------')
            print('\nresult: ', result)
            return result, result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return {
                "code": 500,
                "message": "booking.py internal error: " + ex_str
            }, 500

    # if reached here, not a JSON request.
    return {
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }, 400


def processCreateBooking(createBooking):
    blocked_slots_URL = BLOCKED_SLOTS_URL
    print('\n\n-----Invoking blocked_slots microservice-----')
    blocked_slots_URL = blocked_slots_URL + "?" + "date=" + createBooking['date'] + "&slotNo=" + str(createBooking['slotNo']) + "&doctorID=" + createBooking['doctorID'] + "clinicID=" + createBooking['clinicID']
    blocked_slots_result, blocked_slots_response_code = invoke_http(blocked_slots_URL, method="GET", json=createBooking)
    message = json.dumps(blocked_slots_result)
    print('blocked_slots_results', blocked_slots_result)

    if len(blocked_slots_result['data']) != 0:
        return {
            "code": 500,
            "data": {"blocked_slots_result": blocked_slots_result},
            "message": "Booking creation failure sent for error handling. Because blocked_slots are found"
        }

    print('\n-----Invoking booking microservice-----')
    booking_result, booking_response_code = invoke_http(BOOKING_URL, method='POST', json=createBooking)
    print('booking_result:', booking_result)
    message = json.dumps(booking_result)
    if booking_response_code not in range(200, 300):
        # Inform the log microservice NOT DONE YET
        return {
        "code": 500,
        "data": {"blocked_slots_result": blocked_slots_result,
                    "booking_result": booking_result},
        "message": "Booking creation failure sent for error handling. Because of booking_result failure"
    }
    else:
        return {
        "code": 200,
        "data": {"blocked_slots_result": blocked_slots_result,
                    "booking_result": booking_result},
        "message": "Booking creation Success"
    }
    
@app.route("/deleteBooking", methods=["DELETE"])
def delete_booking():
    deleteBooking = request.args.get('bookingID')
    
    print("\nReceived a delete booking request in URL:", deleteBooking)
    result = processDeleteBooking(deleteBooking)
    print(result)
    if result['code'] == 200:
        processed_result = {}
        print("LALALALALALAL")
        print(result['data']['retrieve_booking_result']['data'][0]['doctorEmail'])
        processed_result['doctorEmail'] = result['data']['retrieve_booking_result']['data'][0]['doctorEmail']
        processed_result['doctorName'] = result['data']['retrieve_booking_result']['data'][0]['doctorName']
        processed_result['patientEmail'] = result['data']['retrieve_booking_result']['data'][0]['patientEmail']
        processed_result['patientName'] = result['data']['retrieve_booking_result']['data'][0]['patientName']
        processed_result['date'] = result['data']['retrieve_booking_result']['data'][0]['date']
        processed_result['slotNo'] = result['data']['retrieve_booking_result']['data'][0]['slotNo']
        processed_result['code'] = result['code']
        result = processed_result
    print('\n------------------------')
    print('\nresult: ', result)

    return result, result["code"]


def processDeleteBooking(deleteBooking):
    booking_URL = BOOKING_URL
    print('\n-----Invoking booking microservice-----')
    booking_URL = booking_URL + "?bookingID=" + str(deleteBooking)
    print(booking_URL)
    retrieve_booking_result, retrieve_booking_response_code = invoke_http(booking_URL, method="GET", json=deleteBooking)
    print('retrieve_booking_result', retrieve_booking_result)
    message = json.dumps(retrieve_booking_result)
    if retrieve_booking_response_code not in range(200, 300):
            # Inform the log microservice NOT DONE YET
            return {
            "code": 500,
            "data": {"retrieve_booking_result": retrieve_booking_result,
                     },
            "message": "Cannot find booking."
        }
    else:
        delete_booking_result, delete_booking_response_code = invoke_http(booking_URL, method="DELETE", json=deleteBooking)
        print('delete_booking_result', delete_booking_result)
        if delete_booking_response_code not in range(200, 300):
            # Inform the log microservice NOT DONE YET
            return {
            "code": 500,
            "data": {"retrieve_booking_result": retrieve_booking_result,
                     "delete_booking_result": delete_booking_result},
            "message": "Cannot delete booking."
        }
        else:
            return {
            "code": 200,
            "data": {"retrieve_booking_result": retrieve_booking_result,
                     "delete_booking_result": delete_booking_result},
            "message": "Deletion Success"
        }


@app.route("/complete", methods=["PATCH"])
@with_logging
def complete_booking():
    # Change booking status to completed
    # Send notification
    
    return {
        "message": "Booking completed successfully",
        "data": {
            "retrieve_booking_result": json.dumps({
                "message": "Booking completed successfully."
            })
        }
    }, 200


# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for creating a booking...")
    app.run(host="0.0.0.0", port=5000, debug=True)
    # Notes for the parameters:
    # - debug=True will reload the program automatically if a change is detected;
    #   -- it in fact starts two instances of the same flask program,
    #       and uses one of the instances to monitor the program changes;
    # - host="0.0.0.0" allows the flask program to accept requests sent from any IP/host (in addition to localhost),
    #   -- i.e., it gives permissions to hosts with any IP to access the flask program,
    #   -- as long as the hosts can already reach the machine running the flask program along the network;
    #   -- it doesn't mean to use http://0.0.0.0 to access the flask program.


