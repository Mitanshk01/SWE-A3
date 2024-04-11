from message_broker import MessageBroker

class BookingResponseBroker:
    def __init__(self):
        self.broker = MessageBroker()
        self.broker.create_topic_exchange('booking_response')

    def publish_response(self, message):
        self.broker.publish_message('booking_response', '', message)

    def consume_responses(self, callback):
        self.broker.create_queue('booking_response_queue')
        self.broker.bind_queue_to_exchange('booking_response_queue', 'booking_response', '')
        self.broker.consume_messages('booking_response_queue', callback)