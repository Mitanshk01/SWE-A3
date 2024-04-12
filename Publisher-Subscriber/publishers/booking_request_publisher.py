import pika
import json

class BookingRequestPublisher:
    def __init__(self, exchange_name):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.exchange_name = exchange_name
        self.channel.exchange_declare(exchange=exchange_name, exchange_type='fanout')

    def publish_message(self, message):
        self.channel.basic_publish(exchange=self.exchange_name, routing_key='', body=json.dumps(message))

    def close_connection(self):
        self.connection.close()
