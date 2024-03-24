import json
import pika
from db import db
from flask import jsonify
from models import Log
import uuid

import amqp_connection

log_queue_name = 'All_Logs' 

def receiveLog(channel):
    try:
        channel.basic_consume(queue=log_queue_name, on_message_callback=callback, auto_ack=True)
        print('error microservice: Consuming from queue:', log_queue_name)
        channel.start_consuming() 
    
    except pika.exceptions.AMQPError as e:
        print(f"error microservice: Failed to connect: {e}") 

    except KeyboardInterrupt:
        print("error microservice: Program interrupted by user.")


def callback(channel, method, properties, body): 
    print("Received Log From:" + __file__)
    data = json.loads(body)
    print(data)
    print()

# create record in database
    log = Log(
        logID = str(uuid.uuid4()),
        timeStamp = data['timeStamp'],
        logMsg =data['msg']
    )

    db.session.add(log)
    db.session.commit()
    
    return jsonify(log.json()), 201

# define error and success logs?
# def processSuccess(Msg): 
# def processError(Msg):


if __name__ == "__main__":     
    print("error microservice: Getting Connection")
    connection = amqp_connection.create_connection() 
    print("error microservice: Connection established successfully")
    channel = connection.channel()
    receiveLog(channel)
