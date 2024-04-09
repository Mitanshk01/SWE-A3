# client.py

import pika

def receive_response(ch, method, properties, body):
    print("Received response:", body)

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='handler')
    channel.basic_consume(queue='handler', on_message_callback=receive_response, auto_ack=True)
    
    num_tickets_to_book = 2  # Change this value as per your requirement
    channel.basic_publish(exchange='', routing_key='booking_request', body=str(num_tickets_to_book))
    print("Booking request sent for {} tickets.".format(num_tickets_to_book))

    print("Waiting for response...")
    channel.start_consuming()

if __name__ == '__main__':
    main()
