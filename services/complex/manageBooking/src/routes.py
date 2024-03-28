from flask import Flask, Blueprint, request, jsonify
import json
import uuid
from flask_cors import CORS
import os, sys
import requests
from invokes import invoke_http
import pika
import json
import amqp_connection

app = Flask(__name__)
CORS(app)

exchangename = "log_fanout"
exchangetype= "fanout" 

connection = amqp_connection.create_connection() 
channel = connection.channel()

blocked_slots_URL = "http://localhost:50000/"
# log_URL = 
# noti_URL =
booking_URL = "http://localhost:5005/bookings"

#if the exchange is not yet created, exit the program
if not amqp_connection.check_exchange(channel, exchangename, exchangetype):
    print("\nCreate the 'Exchange' before running this microservice. \nExiting the program.")
    sys.exit(0)  # Exit with a success status

@app.route("/createBooking")
def index():
    return "createBooking Comple Microservice is running"

#booking routes

@app.route("/createBooking", methods=["POST"])
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
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "booking.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


def processCreateBooking(createBooking):
    global blocked_slots_URL
    print('\n\n-----Invoking blocked_slots microservice-----')
    blocked_slots_URL = blocked_slots_URL + "?" + "date=" + createBooking['date'] + "&slotNo=" + str(createBooking['slotNo']) + "&doctorID=" + createBooking['doctorID'] + "clinicID=" + createBooking['clinicID']
    blocked_slots_result, blocked_slots_response_code = invoke_http(blocked_slots_URL, method="GET", json=createBooking)
    print('blocked_slots_results', blocked_slots_result)
    if blocked_slots_result['message'] != "No slots found.":
        print('\n\n-----Publishing the (log error) message with routing_key=#-----')
        channel.basic_publish(exchange=exchangename, routing_key="#", 
                body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        print("\nCreate Booking status ({:d}) published to the RabbitMQ Exchange:".format(
                blocked_slots_response_code), blocked_slots_result)
        return {
            "code": 500,
            "data": {"blocked_slots_result": blocked_slots_result},
            "message": "Booking creation failure sent for error handling. Because blocked_slots are found"
        }

    if blocked_slots_result['message'] == "No slots found.":
        print('\n-----Invoking booking microservice-----')
        booking_result, booking_response_code = invoke_http(booking_URL, method='POST', json=createBooking)
        print('booking_result:', booking_result)
        message = json.dumps(booking_result)
        if booking_response_code not in range(200, 300):
            # Inform the log microservice NOT DONE YET
            print('\n\n-----Publishing the (log error) message with routing_key=#-----')
            channel.basic_publish(exchange=exchangename, routing_key="#", 
                body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
     
            print("\nCreate Booking status ({:d}) published to the RabbitMQ Exchange:".format(
                booking_response_code), booking_result)
            return {
            "code": 500,
            "data": {"blocked_slots_result": blocked_slots_result,
                     "booking_result": booking_result},
            "message": "Booking creation failure sent for error handling. Because of booking_result failure"
        }
        else:
            print('\n\n-----Publishing the (Log) message with routing_key=#-----')
            channel.basic_publish(exchange=exchangename, routing_key="#", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
     
            print("\nCreate Booking status ({:d}) published to the RabbitMQ Exchange:".format(
            booking_response_code), booking_result)
            return {
            "code": 200,
            "data": {"blocked_slots_result": blocked_slots_result,
                     "booking_result": booking_result},
            "message": "Booking creation Success"
        }
    
@app.route("/deleteBooking", methods=["DELETE"])
def delete_booking():
    deleteBooking = request.args.get('patientID')
    # Simple check of input format and data of the request are JSON
    
    print("\nReceived a delete booking request in URL:", deleteBooking)

    result = processDeleteBooking(deleteBooking)

    #if result['code'] == 200:
        #processed_result[] = result[]
    print('\n------------------------')
    print('\nresult: ', result)
    return jsonify(result), result["code"]


def processDeleteBooking(deleteBooking):
    global booking_URL
    print('\n-----Invoking booking microservice-----')
    retrieve_booking_result, retrieve_booking_response_code = invoke_http(booking_URL, method="GET", json=deleteBooking)
    print('retrieve_booking_result', retrieve_booking_result)
    message = json.dumps(retrieve_booking_result)
    if retrieve_booking_response_code not in range(200, 300):
            # Inform the log microservice NOT DONE YET
            print('\n\n-----Publishing the (log error) message with routing_key=#-----')
            channel.basic_publish(exchange=exchangename, routing_key="#", 
                body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
     
            print("\nCreate Booking status ({:d}) published to the RabbitMQ Exchange:".format(
                retrieve_booking_response_code), retrieve_booking_result)
            return {
            "code": 500,
            "data": {"retrieve_booking_result": retrieve_booking_result,
                     },
            "message": "Cannot find booking."
        }
    else:
        print('\n\n-----Publishing the (Log) message with routing_key=#-----')
        channel.basic_publish(exchange=exchangename, routing_key="#", 
        body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
     
        print("\nCreate Booking status ({:d}) published to the RabbitMQ Exchange:".format(retrieve_booking_response_code), retrieve_booking_result)
        delete_booking_result, delete_booking_response_code = invoke_http(booking_URL, method="DELETE", json=deleteBooking)
        print('delete_booking_result', delete_booking_result)
        if delete_booking_response_code not in range(200, 300):
            # Inform the log microservice NOT DONE YET
            print('\n\n-----Publishing the (log error) message with routing_key=#-----')
            channel.basic_publish(exchange=exchangename, routing_key="#", 
                body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
     
            print("\nCreate Booking status ({:d}) published to the RabbitMQ Exchange:".format(
                delete_booking_response_code), delete_booking_result)
            return {
            "code": 500,
            "data": {"retrieve_booking_result": retrieve_booking_result,
                     "delete_booking_result": delete_booking_result},
            "message": "Cannot delete booking."
        }
        else:
            print('\n\n-----Publishing the (Log) message with routing_key=#-----')
            channel.basic_publish(exchange=exchangename, routing_key="#", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
     
            print("\nCreate Booking status ({:d}) published to the RabbitMQ Exchange:".format(
            delete_booking_response_code), delete_booking_result)
            return {
            "code": 200,
            "data": {"retrieve_booking_result": retrieve_booking_result,
                     "delete_booking_result": delete_booking_result},
            "message": "Booking creation Success"
        }



   

# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for creating a booking...")
    app.run(host="0.0.0.0", port=5006, debug=True)
    # Notes for the parameters:
    # - debug=True will reload the program automatically if a change is detected;
    #   -- it in fact starts two instances of the same flask program,
    #       and uses one of the instances to monitor the program changes;
    # - host="0.0.0.0" allows the flask program to accept requests sent from any IP/host (in addition to localhost),
    #   -- i.e., it gives permissions to hosts with any IP to access the flask program,
    #   -- as long as the hosts can already reach the machine running the flask program along the network;
    #   -- it doesn't mean to use http://0.0.0.0 to access the flask program.


