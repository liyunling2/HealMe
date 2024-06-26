import json
import os
import pika
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
from templates import create_html_email  # Assuming you have this from your previous setup
import logging
import time

load_dotenv()

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
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', "%Y-%m-%d"))
logging.basicConfig(level=logging.INFO, handlers=[handler])
handler.addFilter(LibraryLogFilter())

# Function to establish AMQP connection
hostname = os.getenv('AMQP_HOST') or "rabbitmq"
port = os.getenv('AMQP_PORT') or 5672

def get_amqp_connection(max_retries=12, retry_interval=5):
    logging.info('Notification amqp_connection: Create_connection')
    
    retries = 0
    connection = None

    while retries < max_retries:
        try:
            logging.info('Notification amqp_connection: Trying connection')
            connection = pika.BlockingConnection(pika.ConnectionParameters
                                (host=hostname, port=port,
                                 heartbeat=3600, blocked_connection_timeout=3600)) 
            logging.info("Complex Manage Booking amqp_connection: Connection established successfully")
            break 

        except pika.exceptions.AMQPConnectionError as e:
            logging.warning(f"Notification amqp_connection: Failed to connect: {e}")
            retries += 1
            logging.warning(f"Notification amqp_connection: Retrying in {retry_interval} seconds...")
            time.sleep(retry_interval)
    
    if connection is None:
        raise Exception("Notification unable to establish a connection to RabbitMQ after multiple attempts")
    
    return connection


# Callback function to process messages
def on_message(channel, method_frame, header_frame, body):
    logging.info("------------Receiving an email request message------------")
    try:
        data = json.loads(body)
        message = Mail(
            from_email=data['from'],
            to_emails=data['to'],
            subject=data['subject'],
            html_content=create_html_email(**data['content'])
        )
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        sg.send(message)
        logging.info("Email sent successfully")
    except Exception as e:
        logging.error(f"Failed to send email: {str(e)}")

# Setup and start listening to the queue
def start_consuming():
    connection = get_amqp_connection()
    channel = connection.channel()
    queue_name = 'email_requests'  # The queue name should match what your producers are using
    
    # Ensure the queue exists
    channel.queue_declare(queue=queue_name, durable=True)
    
    # Start consuming messages
    channel.basic_consume(queue=queue_name, on_message_callback=on_message, auto_ack=True)
    logging.info(f"[*] Waiting for messages in {queue_name}. To exit press CTRL+C")
    channel.start_consuming()

if __name__ == "__main__":
    start_consuming()
