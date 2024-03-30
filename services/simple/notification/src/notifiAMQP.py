import json
import os
import pika
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
from templates import create_html_email  # Assuming you have this from your previous setup

load_dotenv()

# Function to establish AMQP connection
def get_amqp_connection():
    connection_params = pika.ConnectionParameters(
        host=os.getenv('AMQP_HOST'),
        port=int(os.getenv('AMQP_PORT', 5672)),
        virtual_host=os.getenv('AMQP_VHOST', '/'),
        credentials=pika.PlainCredentials(os.getenv('AMQP_USERNAME'), os.getenv('AMQP_PASSWORD'))
    )
    return pika.BlockingConnection(connection_params)

# Callback function to process messages
def on_message(channel, method_frame, header_frame, body):
    print("Received an email request message")
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
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

# Setup and start listening to the queue
def start_consuming():
    connection = get_amqp_connection()
    channel = connection.channel()
    queue_name = 'email_requests'  # The queue name should match what your producers are using
    
    # Ensure the queue exists
    channel.queue_declare(queue=queue_name, durable=True)
    
    # Start consuming messages
    channel.basic_consume(queue=queue_name, on_message_callback=on_message, auto_ack=True)
    print(f"[*] Waiting for messages in {queue_name}. To exit press CTRL+C")
    channel.start_consuming()

if __name__ == "__main__":
    start_consuming()
