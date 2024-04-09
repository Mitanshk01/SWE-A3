# message_broker.py

import pika

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='booking_request')
    channel.queue_declare(queue='handler')
    print("Message broker is ready.")
    
    try:
        # Keep the main thread running indefinitely
        while True:
            pass
    except KeyboardInterrupt:
        print("Shutting down message broker.")
        connection.close()

if __name__ == '__main__':
    main()