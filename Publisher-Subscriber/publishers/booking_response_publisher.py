from message_broker import MessageBroker

class BookingResponsePublisher:
    def __init__(self):
        self.broker = MessageBroker()

    def publish(self, message):
        self.broker.publish_message('booking_response', '', message)