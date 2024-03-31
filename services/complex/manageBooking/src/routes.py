import json
import logging
from utils import get_log_message_dict
import os
import sys
import uuid

import amqp_connection
import pika
import requests
from flask import Blueprint, Flask, jsonify, request
from flask_cors import CORS
from invokes import invoke_http, send_notification, queue_notification, format_notification_data

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
        try:
            body = get_log_message_dict((response, code))
        
            channel.basic_publish(exchange=exchangename, routing_key="#",
                              body=json.dumps(body), properties=pika.BasicProperties(delivery_mode=2))

        except Exception as e:
            logging.error(str(e))

        finally:
            return response, code

    return with_log_fn

def with_notification(action="confirmed", accessor=lambda x: x, channel=channel):
    def with_notification_wrapper(route_handler_fn):
        @wraps(route_handler_fn)
        def with_notification_fn(*args, **kwargs):
            response, code = route_handler_fn(*args, **kwargs)
            try:
                if (code >= 200 and code < 300):
                    booking_data = accessor(response["data"])

                    to_email = booking_data["patientEmail"]
                    date = booking_data["date"][:-13]
                    time_num =  7 + (booking_data["slotNo"] - 1) * 0.5
                    time_str = f"{int(time_num)}:{'00' if time_num % 1 == 0 else '30'}"
                    clinic_name = booking_data["clinicName"]

                    # queue_notification(f"Your booking has been {action}", f"Your booking on {date}, {time_str} at {clinic_name} has been {action}", to_email, channel)
                    data = format_notification_data(f"Your booking has been {action}", f"Your booking on {date}, {time_str} at {clinic_name} has been {action}", to_email)

                    logging.info("Sending notification request to the queue")
                    channel.basic_publish(exchange="direct_exchange", routing_key="email.notification.request",
                                    body=json.dumps(data), properties=pika.BasicProperties(delivery_mode=2))

                    # noti_code = None
                    # tries = 0

                    # while noti_code != 200 and tries < 3:
                    #     noti_response, noti_code = send_notification(f"Your booking has been {action}", f"Your booking on {date}, {time_str} at {clinic_name} has been {action}", to_email)
                    #     tries += 1
                    
                    # if noti_code != 200:
                    #     raise Exception(f"Notification failed with code {noti_code}" + str(noti_response))

                
            except Exception as e:
                logging.error(str(e))
            
            return response, code

        return with_notification_fn
    
    return with_notification_wrapper
            
        
BLOCKED_SLOTS_URL = os.environ.get("BLOCKED_SLOTS_URL")
# noti_URL =
BOOKING_URL = os.environ.get("BOOKING_URL")
PROFILE_URL = os.environ.get("PROFILE_URL")
CLINIC_URL = os.environ.get("CLINIC_URL")


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
@with_notification("confirmed", lambda x: x["booking_result"]["data"])
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
    #patient ID ensure its in patient DB
    #clinic ID exists
    #doctor ID exists
    profile_URL = PROFILE_URL
    blocked_slots_URL = BLOCKED_SLOTS_URL
    print('\n\n-----Invoking Profile for Patient microservice-----')
    profile_URL = profile_URL + "/patients/" + createBooking['patientID'] 
    patient_result, patient_response_code = invoke_http(profile_URL, method="GET", json=createBooking)
    
    if patient_response_code not in range(200, 300):
        return {
            "code": 500,
            "data": {"patient_result": patient_result},
            "message": "Booking creation failure sent for error handling. Because patientID doesnt exist"
        }
    print('\n\n-----Invoking Profile for Doctor microservice-----')
    profile_URL = PROFILE_URL
    profile_URL = profile_URL + "/doctors/" + createBooking['doctorID']
    doctor_result, doctor_response_code = invoke_http(profile_URL, method="GET", json=createBooking)
    if doctor_response_code not in range(200, 300) or doctor_result['data']['clinicID'] != createBooking['clinicID']:
        return {
            "code": 500,
            "data": {"patient_result": patient_result,
                     "doctor_result": doctor_result},
            "message": "Booking creation failure sent for error handling. Because doctorID doesnt exist or doctor does not belong to this clinicID"
        }
    print('\n\n-----Invoking blocked_slots microservice-----')
    blocked_slots_URL = blocked_slots_URL + "?" + "date=" + createBooking['date'] + "&slotNo=" + str(createBooking['slotNo']) + "&doctorID=" + createBooking['doctorID'] + "clinicID=" + createBooking['clinicID']
    blocked_slots_result, blocked_slots_response_code = invoke_http(blocked_slots_URL, method="GET", json=createBooking)
    message = json.dumps(blocked_slots_result)
    print('blocked_slots_results', blocked_slots_result)

    if len(blocked_slots_result['data']) != 0:
        return {
            "code": 500,
            "data": {"patient_result": patient_result,
                     "doctor_result": doctor_result,
                "blocked_slots_result": blocked_slots_result},
            "message": "Booking creation failure sent for error handling. Because blocked_slots are found"
        }

    print('\n-----Invoking booking microservice-----')
    booking_result, booking_response_code = invoke_http(BOOKING_URL, method='POST', json=createBooking)
    print('booking_result:', booking_result)
    message = json.dumps(booking_result)
    if booking_response_code not in range(200, 300):
        return {
        "code": 500,
        "data": {"patient_result": patient_result,
                     "doctor_result": doctor_result,
                "blocked_slots_result": blocked_slots_result,
                "booking_result": booking_result},
        "message": "Booking creation failure sent for error handling. Because of booking_result failure"
    }
    else:
        return {
        "code": 200,
        "data": {"patient_result": patient_result,
                     "doctor_result": doctor_result,
                "blocked_slots_result": blocked_slots_result,
                "booking_result": booking_result},
        "message": "Booking creation Success"
    }
    
@app.route("/deleteBooking", methods=["DELETE"])
@with_logging
@with_notification("cancelled")
def delete_booking():
    deleteBooking = request.args.get('bookingID')
    
    print("\nReceived a delete booking request in URL:", deleteBooking)
    result = processDeleteBooking(deleteBooking)
    print(result)
    code = result["code"]
    if code == 200:
        processed_result = result['data']['retrieve_booking_result']['data'][0]
        result = processed_result

    print('\n------------------------')
    print('\nresult: ', result)

    return {
        "message": "Booking deletion success" if code == 200 else "Booking deletion failure",
        "data": result
    }, code


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


@app.route("/complete/<string:booking_id>", methods=["PUT"])
@with_logging
@with_notification("completed. Please rate the doctor.")
def complete_booking(booking_id):
    # Change booking status to completed
    try:
        response, code = invoke_http(BOOKING_URL + f"/{booking_id}", method="PATCH", json={"bookingStatus": "Completed"})
        return response, code

    except Exception as e:
        return {
            "message": "An error occurred updating the booking."
        }, 500

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


