# from message_broker import MessageBroker
from brokers.booking_request_broker import BookingRequestBroker

class BookingRequestPublisher:
    def __init__(self):
        self.broker = BookingRequestBroker()

    def publish(self, message):
        self.broker.publish_request(message)
        print(f"In publisher: Published booking request: {message}")