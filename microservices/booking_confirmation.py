import pika, json
from utilities import update_status

def on_confirmation(ch, method, properties, body):
    """
    Callback function invoked when a booking confirmation message is received.

    Parameters:
        ch (pika.channel.Channel): The channel object.
        method (pika.spec.Basic.Deliver): Delivery information.
        properties (pika.spec.BasicProperties): Message properties.
        body (bytes): The message body containing the confirmation data.

    Note:
        This function processes the booking confirmation message, updates the
        status of the corresponding booking request to 'Confirmed', and acknowledges
        the message.
    """
    confirmation_data = json.loads(body)
    request_id = confirmation_data['request_id']
    update_status(request_id, "Confirmed")
    print(f"Booking confirmed: {confirmation_data}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='bookingExchange', exchange_type='direct')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='bookingExchange', queue=queue_name, routing_key='booking_confirmation')
channel.basic_consume(queue=queue_name, on_message_callback=on_confirmation)
print("Booking Confirmation Service is waiting for confirmations.")

channel.start_consuming()
