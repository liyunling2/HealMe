import time
import pika
from os import environ
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
logging.getLogger('werkzeug').setLevel(logging.ERROR)

hostname = environ.get('hostname') or "rabbitmq"
port = environ.get('port') or 5672

def create_connection(max_retries=12, retry_interval=5):
    logging.info('Complex Manage Booking amqp_connection: Create_connection')
    
    retries = 0
    connection = None

    while retries < max_retries:
        try:
            logging.info('Complex Manage Booking amqp_connection: Trying connection')
            connection = pika.BlockingConnection(pika.ConnectionParameters
                                (host=hostname, port=port,
                                 heartbeat=3600, blocked_connection_timeout=3600)) 
            logging.info("Complex Manage Booking amqp_connection: Connection established successfully")
            break 

        except pika.exceptions.AMQPConnectionError as e:
            logging.warning(f"Complex Manage Booking amqp_connection: Failed to connect: {e}")
            retries += 1
            logging.warning(f"Complex Manage Booking amqp_connection: Retrying in {retry_interval} seconds...")
            time.sleep(retry_interval)
    
    if connection is None:
        raise Exception("Complex Manage Booking unable to establish a connection to RabbitMQ after multiple attempts")
    
    return connection

def check_exchange(channel, exchangename, exchangetype):
    try:    
        channel.exchange_declare(exchangename, exchangetype, durable=True, passive=True) 
                       
    except Exception as e:
        logging.error('Exception:', e)
        return False
    return True


if __name__ == "__main__":
    create_connection()