import amqp_connection
import json
import pika
# from os import environ

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

    processSuccess(body)

    processError(body)


def processSuccess(Msg):
    
    
def processError(Msg):



if __name__ == "__main__":     
    print("error microservice: Getting Connection")
    connection = amqp_connection.create_connection() 
    print("error microservice: Connection established successfully")
    channel = connection.channel()
    receiveLog(channel)
