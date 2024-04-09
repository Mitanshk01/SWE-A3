# booking_service.py

import pika

def callback(ch, method, properties, body):
    # Simulate processing of booking request
    venue_capacity = 500  # Capacity of the venue
    num_tickets_sold = 100  # Number of tickets already sold
    booking_request = int(body)

    if num_tickets_sold + booking_request <= venue_capacity:
        response = "Booking confirmed for {} tickets.".format(booking_request)
    else:
        response = "Not enough available tickets for booking."

    ch.basic_publish(exchange='', routing_key='handler', body=response)

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='booking_request')
    channel.basic_consume(queue='booking_request', on_message_callback=callback, auto_ack=True)
    print("Booking service is waiting for booking requests...")
    channel.start_consuming()

if __name__ == '__main__':
    main()
