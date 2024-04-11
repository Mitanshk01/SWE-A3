from message_broker import MessageBroker

class BookingRequestBroker:
    def __init__(self):
        self.broker = MessageBroker()
        self.broker.create_topic_exchange('booking_request')

    def publish_request(self, message):
        print("In Broker: Message publisher")
        self.broker.publish_message('booking_request', '', message)

    def consume_requests(self, callback):
        self.broker.create_queue('booking_request_queue')
        self.broker.bind_queue_to_exchange('booking_request_queue', 'booking_request', '')
        self.broker.consume_messages('booking_request_queue', callback)