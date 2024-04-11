from message_broker import MessageBroker
from utilities import get_status_from_db
import json

class BookingResponseSubscriber:
    def __init__(self):
        self.broker = MessageBroker()

    def handle_message(self, ch, method, properties, body):
        # Extract request ID from the message body
        request_id = body.decode()
        print(f"Received request ID: {request_id}")

        # Check the status of the request ID in the database
        status = get_status_from_db(request_id)
        print(f"Status for request ID {request_id}: {status}")


        # Publish the status as a response message
        response_message = {'request_id': request_id, 'status': status}
        self.broker.publish_message('booking_response', '', json.dumps(response_message))

    def start_consuming(self):
        self.broker.create_queue('booking_response_queue')
        self.broker.bind_queue_to_exchange('booking_response_queue', 'booking_response', '')
        self.broker.consume_messages('booking_response_queue', self.handle_message)