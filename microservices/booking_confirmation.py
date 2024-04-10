import pika, json
from utilities import update_request_status, create_venue_occupancy_table,\
    get_venue_occupancy, update_venue_occupancy

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
    venue_id = int(confirmation_data['venueId'])
    seats = int(confirmation_data['seats'])

    # Check if seats can be booked without exceeding max occupancy
    if seats_can_be_booked(venue_id, seats):
        update_request_status(request_id, "Confirmed")
        update_venue_occupancy(venue_id, seats)
        print(f"Booking confirmed: {confirmation_data}")
    else:
        update_request_status(request_id, "Denied")
        print(f"Booking denied: {confirmation_data}")

    ch.basic_ack(delivery_tag=method.delivery_tag)

def seats_can_be_booked(venue_id, seats):
    """
    Check if the given number of seats can be booked for the specified venue
    without exceeding the maximum occupancy.

    Parameters:
        venue_id (int): The ID of the venue.
        seats (int): The number of seats requested.

    Returns:
        bool: True if seats can be booked, False otherwise.
    """
    venue_occupancy = get_venue_occupancy(venue_id)
    if venue_occupancy:
        max_occupancy = int(venue_occupancy[0])
        current_occupancy = int(venue_occupancy[1])
        if current_occupancy + seats <= max_occupancy:
            return True
    return False

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='bookingExchange', exchange_type='direct')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='bookingExchange', queue=queue_name, routing_key='booking_confirmation')
channel.basic_consume(queue=queue_name, on_message_callback=on_confirmation)
print("Booking Confirmation Service is waiting for confirmations.")

channel.start_consuming()
