import json
import pika
from flask import jsonify
import amqp_connection
import logging
from logging.handlers import RotatingFileHandler

class LibraryLogFilter(logging.Filter):
    def filter(self, record):
        # Filter out log records
        if record.name.startswith('pika.') or record.name == 'AMQP':
            return False
        return True
    
# 1 MB max size, keep 5 backups
handler = RotatingFileHandler(filename='../../../app_logs/application.log', maxBytes=1024*1024, backupCount=5) 
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logging.basicConfig(level=logging.INFO, handlers=[handler])
handler.addFilter(LibraryLogFilter())

log_queue_name = 'All_Logs' 
channel = None

def receiveLog(channel):
    try:
        channel.basic_consume(queue=log_queue_name, on_message_callback=callback, auto_ack=True)
        logging.info('Log microservice ready to consume from %s', log_queue_name)
        channel.start_consuming() 
    
    except pika.exceptions.AMQPError as e:
        logging.error(f"Log microservice: Failed to connect: %s {e}")

    except KeyboardInterrupt:
        logging.error("Log microservice: Program interrupted by user.")
        

def callback(channel, method, properties, body): 
    logging.info("------------Receiving Log------------")
    try:
        data = json.loads(body)
        logging.info("Message Received: %s", json.dumps(data, indent=4))
        print()
    except Exception as e:
        # Log any errors that occur during processing
        logging.error("Error processing log message: %s", e)


if __name__ == "__main__" and channel == None:     
    logging.info("Log microservice: Getting Connection")
    connection = amqp_connection.create_connection() 
    logging.info("Log microservice: Connection established successfully")
    channel = connection.channel()
    receiveLog(channel)
