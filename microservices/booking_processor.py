import pika
import json
import time

def process_booking(body):
    booking_data = json.loads(body)
    # Simulate processing time and logic
    print(f"Processed booking request: {booking_data}")
    return booking_data  # In a real scenario, we'd update this data as needed

def on_request(ch, method, properties, body):
    print("Received booking request:", body)
    processed_booking = process_booking(body)

    ch.basic_publish(exchange='bookingExchange',
                     routing_key='booking_confirmation',
                     body=json.dumps(processed_booking))
    ch.basic_ack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='bookingExchange', exchange_type='direct')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='bookingExchange', queue=queue_name, routing_key='booking_request')

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue_name, on_message_callback=on_request)

print("Booking Processor Service is waiting for booking requests.")
channel.start_consuming()