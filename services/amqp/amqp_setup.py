import time
import pika
from os import environ
import logging
from logging.handlers import RotatingFileHandler

# 1 MB max size, keep 5 backups
handler = RotatingFileHandler(filename='../app_logs/application.log', maxBytes=1024*1024, backupCount=5) 
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logging.basicConfig(level=logging.INFO, handlers=[handler])

hostname = environ.get('hostname') or "localhost"
port = environ.get('port')  or 5672
exchangename = "log_fanout"
exchangetype = "fanout"
 

def create_connection(max_retries=12, retry_interval=5):
    logging.info('amqp_setup: create_connection')
    
    retries = 0
    connection = None
    
    while retries < max_retries:
        try:
            logging.info('amqp_setup: Trying connection')
            
            connection = pika.BlockingConnection(pika.ConnectionParameters
                                (host=hostname, port=port,
                                 heartbeat=3600, blocked_connection_timeout=3600)) 
            logging.info("amqp_setup: Connection established successfully")
            break  

        except pika.exceptions.AMQPConnectionError as e:
            logging.error(f"amqp_setup: Failed to connect: {e}")
            retries += 1
            logging.error(f"amqp_setup: Retrying in {retry_interval} seconds...")
            time.sleep(retry_interval)

    if connection is None:
        logging.error("amqp_setup: Unable to establish a connection to RabbitMQ after multiple attempts.")

    return connection

def create_channel(connection):
    logging.info('amqp_setup:create_channel')
    channel = connection.channel()
    logging.info('amqp_setup:create exchange')
    channel.exchange_declare(exchange=exchangename, exchange_type=exchangetype, durable=True) 

    return channel


def create_queue(channel):
    logging.info('amqp_setup:create queues')
    create_log_queue(channel)

  
def create_log_queue(channel):
    logging.info('amqp_setup:create_activity_log_queue')
    log_queue_name = 'All_Logs'
    channel.queue_declare(queue=log_queue_name, durable=True) 
    channel.queue_bind(exchange=exchangename, queue=log_queue_name, routing_key='#')


if __name__ == "__main__":  
    connection = create_connection()
    channel = create_channel(connection)
    create_queue(channel)
    
    