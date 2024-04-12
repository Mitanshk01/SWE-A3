from subscribers.booking_request_subscriber import BookingRequestSubscriber
from subscribers.booking_response_subscriber import BookingResponseSubscriber
from publishers.message_publisher import MessagePublisher

class Handler:
    def __init__(self):
        self.booking_request_subscriber = BookingRequestSubscriber('booking_request_exchange', 'booking_request_queue')
        self.booking_response_subscriber = BookingResponseSubscriber('booking_response_exchange', 'booking_response_queue')
        self.message_publisher = MessagePublisher('message_exchange')
    
    def start_consuming(self):
        self.booking_request_subscriber.start_consuming()

    def start_consuming_response(self):
        self.booking_response_subscriber.start_consuming()
