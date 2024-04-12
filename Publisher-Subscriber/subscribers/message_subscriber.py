import pika
import json
from utilities import get_status_from_db

class MessageSubscriber:
    def __init__(self, exchange_name, queue_name):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.exchange_name = exchange_name
        self.queue_name = queue_name
        self.channel.exchange_declare(exchange=exchange_name, exchange_type='fanout')
        self.channel.queue_declare(queue=self.queue_name)
        self.channel.queue_bind(exchange=exchange_name, queue=self.queue_name)
        self.channel.basic_qos(prefetch_count=1)

    def callback(self, ch, method, properties, body):
        print(" [z] Received Message")
        print("The status of request_id", json.loads(body)['request_id'], "is", json.loads(body)['status'])

    def start_consuming(self):
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback, auto_ack=True)
        print(' [^] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def close_connection(self):
        self.connection.close()