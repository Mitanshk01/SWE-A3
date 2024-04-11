import pika
import json
from utilities import start_processing_request, get_status_from_db, update_request_status

def process_booking(body):
    """
    Process a booking request received as JSON data.

    Parameters:
        body (str): The JSON data representing the booking request.

    Returns:
        dict: The processed booking data after any necessary operations.

    Note:
        In a real scenario, this function would perform various processing
        tasks such as validating the booking data, updating a database,
        sending notifications, etc.
        This is the _rationale_ for this extra service
    """
    booking_data = json.loads(body)
    start_processing_request(booking_data)
    # Simulate processing time and logic
    print(f"Processed booking request: {booking_data}")
    return booking_data  # In a real scenario, we'd update this data as needed

def on_request(ch, method, properties, body):
    """
    Callback function invoked when a booking request message is received.

    Parameters:
        ch (pika.channel.Channel): The channel object.
        method (pika.spec.Basic.Deliver): Delivery information.
        properties (pika.spec.BasicProperties): Message properties.
        body (bytes): The message body containing the booking request data.

    Note:
        This function processes the booking request, publishes the processed
        booking data to another exchange, and acknowledges the message.
    """
    print("Received booking request:", body)
    processed_booking = process_booking(body)

    ch.basic_publish(exchange='bookingExchange',
                     routing_key='booking_confirmation',
                     body=json.dumps(processed_booking))
    ch.basic_ack(delivery_tag=method.delivery_tag)

def on_status_check(ch, method, properties, body):
    """
    Callback function invoked when a booking status check request message is received.

    Parameters:
        ch (pika.channel.Channel): The channel object.
        method (pika.spec.Basic.Deliver): Delivery information.
        properties (pika.spec.BasicProperties): Message properties.
        body (bytes): The message body containing the status check request data.

    Note:
        This function processes the status check request, retrieves the status
        from the database, and sends back the status response.
    """
    print("Received status check request:", body)
    status_check_data = json.loads(body)
    request_id = status_check_data.get('request_id')
    status = get_status_from_db(request_id)

    print("Return status at on_status_check", status, "for request ID", request_id)

    # Send back the status response
    response_data = {"request_id": request_id, "status": status}
    ch.basic_publish(exchange='status_exchange',
                     routing_key='status_response_queue',
                     body=json.dumps(response_data))
    
    ch.basic_ack(delivery_tag=method.delivery_tag)

def on_status_update(ch, method, properties, body):
    """
    Callback function invoked when a status update request message is received.

    Parameters:
        ch (pika.channel.Channel): The channel object.
        method (pika.spec.Basic.Deliver): Delivery information.
        properties (pika.spec.BasicProperties): Message properties.
        body (bytes): The message body containing the status update request data.

    Note:
        This function processes the status update request and updates the status
        of the corresponding booking request in the database.
    """
    print("Received status update request:", body)
    status_update_data = json.loads(body)
    request_id = status_update_data.get('request_id')
    status = status_update_data.get('status')

    # Update the status in the database
    update_request_status(request_id, status)

    ch.basic_ack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='bookingExchange', exchange_type='direct')
channel.exchange_declare(exchange='status_exchange', exchange_type='direct')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='bookingExchange', queue=queue_name, routing_key='booking_request')

channel.queue_declare(queue='status_update_queue')
channel.queue_bind(exchange='bookingExchange', queue='status_update_queue', routing_key='status_update')

channel.queue_declare(queue='status_check_request')
channel.queue_bind(exchange='status_exchange', queue='status_check_request', routing_key='status_check_request')

channel.queue_declare(queue='status_response_queue')
channel.queue_bind(exchange='status_exchange', queue='status_response_queue', routing_key='status_response_queue')

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue_name, on_message_callback=on_request)
channel.basic_consume(queue='status_check_request', on_message_callback=on_status_check)
channel.basic_consume(queue='status_update_queue', on_message_callback=on_status_update)

print("Booking Processor Service is waiting for booking requests and status check requests.")
channel.start_consuming()
