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

exchangename = "createBooking_topic" # exchange name
exchangetype="topic" # use a 'topic' exchange to enable interaction

# Instead of hardcoding the values, we can also get them from the environ as shown below
# exchangename = environ.get('exchangename') #order_topic
# exchangetype = environ.get('exchangetype') #topic 

#create a connection and a channel to the broker to publish messages to activity_log, error queues
connection = amqp_connection.create_connection() 
channel = connection.channel()

#if the exchange is not yet created, exit the program
if not amqp_connection.check_exchange(channel, exchangename, exchangetype):
    print("\nCreate the 'Exchange' before running this microservice. \nExiting the program.")
    sys.exit(0)  # Exit with a success status

booking_URL = "http://localhost:5005/bookings"

@app.route("/createBooking")
def index():
    return "createBooking Comple Microservice is running"

#booking routes

#EXTRACT BOOKING, CAN FILTER AS SUCH http://127.0.0.1:5005/bookings?patientID=101&dateOfBooking=2024-03-01
@app.route("/createBooking", methods=["POST"])
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
                "message": "booking.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

def processCreateBooking(createBooking):
    print('\n-----Invoking booking microservice-----')
    booking_result = invoke_http(booking_URL, method='POST', json=createBooking)
    print("hello")
    print('booking_result:', booking_result)

    # Check the order result; if a failure, send it to the error microservice.
    code = booking_result["code"]
    message = json.dumps(booking_result)
    if code not in range(200, 300):
        # Inform the log microservice NOT DONE YET
        print('\n\n-----Publishing the (log error) message with routing_key=#-----')
        channel.basic_publish(exchange=exchangename, routing_key="#", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        # make message persistent within the matching queues until it is received by some receiver 
        # (the matching queues have to exist and be durable and bound to the exchange)

        # - reply from the invocation is not used;
        # continue even if this invocation fails        
        print("\nOrder status ({:d}) published to the RabbitMQ Exchange:".format(
            code), booking_result)
        
        #return error
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
