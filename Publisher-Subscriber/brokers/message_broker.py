import pika

class MessageBroker:
    def __init__(self, host='localhost'):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()

    def create_topic_exchange(self, exchange_name):
        self.channel.exchange_declare(exchange=exchange_name, exchange_type='topic')

    def create_queue(self, queue_name):
        self.channel.queue_declare(queue=queue_name)

    def bind_queue_to_exchange(self, queue_name, exchange_name, routing_key):
        self.channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)

    def publish_message(self, exchange_name, routing_key, message):
        self.channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=message)

    def consume_messages(self, queue_name, callback):
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()
