import pika, json

def update_status(request_id, status):
    with open("request_status_db.json", "r+") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = {}
        data[request_id] = status
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()

def on_confirmation(ch, method, properties, body):
    confirmation_data = json.loads(body)
    request_id = confirmation_data['request_id']
    update_status(request_id, "Confirmed")
    print(f"Booking confirmed: {confirmation_data}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='bookingExchange', exchange_type='direct')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='bookingExchange', queue=queue_name, routing_key='booking_confirmation')
channel.basic_consume(queue=queue_name, on_message_callback=on_confirmation)
print("Booking Confirmation Service is waiting for confirmations.")
channel.start_consuming()