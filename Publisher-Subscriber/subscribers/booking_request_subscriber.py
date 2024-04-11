from message_broker import MessageBroker
from utilities import start_processing_request, update_request_status, get_venue_occupancy
import json

class BookingRequestSubscriber:
    def __init__(self):
        self.broker = MessageBroker()

    def handle_request(self, ch, method, properties, body):
        # Assuming body is a JSON string containing request data
        request_data = json.loads(body)
        print(f"In Subscriber Received booking request: {request_data}")

        # Start processing the request
        start_processing_request(request_data)

        # Check venue occupancy
        venue_id = request_data['venueId']
        seats_requested = request_data['seats']
        max_occupancy, current_occupancy = get_venue_occupancy(venue_id)

        if current_occupancy + seats_requested <= max_occupancy:
            # Venue has available seats, proceed with booking
            update_request_status(request_data['request_id'], 'Confirmed')
            response_message = {'request_id': request_data['request_id'], 'status': 'Confirmed'}
        else:
            # Venue is fully booked, reject booking
            update_request_status(request_data['request_id'], 'Rejected')
            response_message = {'request_id': request_data['request_id'], 'status': 'Rejected'}

        # Publish response
        self.broker.publish_message('booking_response', '', json.dumps(response_message))

    def start_consuming(self):
        self.broker.create_queue('booking_request_queue')
        self.broker.bind_queue_to_exchange('booking_request_queue', 'booking_request', '')
        self.broker.consume_messages('booking_request_queue', self.handle_request)
