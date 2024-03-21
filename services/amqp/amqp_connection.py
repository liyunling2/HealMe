import time
import pika
from os import environ

hostname = environ.get('hostname') or "localhost"
port = environ.get('port')  or 5672

def create_connection(max_retries=12, retry_interval=5):
    print('amqp_connection: Create_connection')
    
    retries = 0
    connection = None

    while retries < max_retries:
        try:
            print('amqp_connection: Trying connection')
            connection = pika.BlockingConnection(pika.ConnectionParameters
                                (host=hostname, port=port,
                                 heartbeat=3600, blocked_connection_timeout=3600)) 
            print("amqp_connection: Connection established successfully")
            break 

        except pika.exceptions.AMQPConnectionError as e:
            print(f"amqp_connection: Failed to connect: {e}")
            retries += 1
            print(f"amqp_connection: Retrying in {retry_interval} seconds...")
            time.sleep(retry_interval)
    
    if connection is None:
        raise Exception("Unable to establish a connection to RabbitMQ after multiple attempts")
    
    return connection

def check_exchange(channel, exchangename, exchangetype):
    try:    
        channel.exchange_declare(exchangename, exchangetype, durable=True, passive=True) 
                       
    except Exception as e:
        print('Exception:', e)
        return False
    return True


if __name__ == "__main__":
    create_connection()